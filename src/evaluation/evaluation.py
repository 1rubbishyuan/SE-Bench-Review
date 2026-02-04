import re
import requests
import ast
import numpy as np
import re
from openai import OpenAI
from string import Template


class EqualityJudge:
    def __init__(self, alg: str, url: str = None, model_name: str = None):
        self.alg = alg
        self.url = url
        self.model_name = model_name

    def parse_ans(self, response: str):
        match = re.search(r"\\boxed\{([^}]*)\}", response)
        if match:
            result = match.group(1)
            return str(result)

    def str_to_list(self, stdout: str):
        safe_env = {
            "array": np.array,
            "dtype": np.dtype,
            "float64": np.float64,
        }
        arr_list = eval(stdout, safe_env)
        try:
            res = [a.tolist() for a in arr_list]
        except:
            res = []
        return res

    def llm_as_judge(self, exe_result: str, ground_truth_list: list):
        judge_prompt = Template(llm_as_judge_prompt).safe_substitute(
            {"exe_result": exe_result, "ground_truth_list": ground_truth_list}
        )
        client = OpenAI(api_key="", base_url=self.url)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": judge_prompt}], model=self.model_name
        )
        response = response.choices[0].message.content
        ans = self.parse_ans(response=response)
        if ans is not None and "true" in ans.lower():
            return True
        else:
            return False

    def exact_match(self, exe_result: str, ground_truth_list: list):
        exe_result_list = exe_result.strip().split("\n")
        return exe_result_list == ground_truth_list

    def judge(self, exe_result: str, ground_truth_list: list):
        if self.alg == "llm_as_judge":
            return self.llm_as_judge(
                exe_result=exe_result, ground_truth_list=ground_truth_list
            )
        elif self.alg == "exact_match":
            return self.exact_match(
                exe_result=exe_result, ground_truth_list=ground_truth_list
            )
        else:
            raise NotImplementedError()


class Evaluator:
    def __init__(self, worker_url: str):
        self.worker_url = worker_url

    def parse_function(self, raw_code: str):
        pattern = r"def\s+([a-zA-Z_]\w*)\s*\("
        try:
            match = re.search(pattern, raw_code)
        except Exception as e:
            raise e
        if match:
            return match.group(1)
        else:
            return ""

    def parse_raw_code_from_response(self, response: str):
        pattern = r"```python\n([\s\S]*?)```"
        matches = re.findall(pattern, response)
        if matches:
            raw_code = matches[-1]
            return raw_code
        else:
            return ""

    def code_preprocess(self, raw_code: str, test_cases: list):
        new_line_start = "    "
        raw_code += """import zwc\n"""
        raw_code += """if __name__== "__main__":\n"""
        test_cases_str_list = []

        for i in range(len(test_cases)):
            test_cases_str_list.append(test_cases[i]["input"])

        function_name = self.parse_function(raw_code=raw_code)
        raw_code += f"""{new_line_start}test_cases = {test_cases}\n"""
        raw_code += f"""{new_line_start}result_list = []\n"""

        for i in range(len(test_cases_str_list)):
            raw_code += f"""{new_line_start}result_list.append({function_name}({test_cases_str_list[i]}))\n"""

        raw_code += f"""{new_line_start}print("====================")\n"""
        raw_code += f"""{new_line_start}for i in range(len(result_list)):\n"""
        raw_code += f"""{new_line_start}{new_line_start}print(result_list[i])\n"""
        raw_code += f"""{new_line_start}{new_line_start}print("#")"""

        return raw_code

    def code_execute(self, code: str):
        return requests.post(self.worker_url, json={"code": code})

    # def evaluate(self, raw_code: str, test_cases: list):
    #     code = self.code_preprocess(raw_code=raw_code, test_cases=test_cases)
    #     exe_result = self.code_execute(code=code)
    #     exe_result = exe_result.json()

    #     if exe_result["stderr"] != "":
    #         return (False, exe_result["stderr"])
    #     else:
    #         exe_result = exe_result["stdout"].split("====================")[-1].strip()
    #         ground_truth_list = []
    #         for i in range(len(test_cases)):
    #             ground_truth_list.append(test_cases[i]["output"])
    #         right = self.equal_judge.judge(
    #             exe_result=exe_result, ground_truth_list=ground_truth_list
    #         )
    #         return (right, exe_result)


if __name__ == "__main__":
    raw_code = """import numpy as np\n\ndef process_sensor_data(sensor_matrix, noise_pattern, threshold):\n    # Convert inputs to numpy arrays\n    sensor_matrix = np.array(sensor_matrix)\n    noise_pattern = np.array(noise_pattern)\n    \n    # Step 1: Compute Kronecker product\n    expanded_matrix = np.kron(sensor_matrix, noise_pattern)\n    \n    # Step 2: Calculate 75th percentile along axis 0\n    percentiles = np.quantile(expanded_matrix, 0.75, axis=0)\n    \n    # Step 3: Filter values that are >= threshold\n    condition = percentiles >= threshold\n    result = np.compress(condition, percentiles)\n    \n    return result\n"""

    test_cases = [
        {
            "input": "sensor_matrix=[[1, 2], [3, 4]], noise_pattern=[[0.5, 1.0], [1.5, 2.0]], threshold=3.0",
            "output": "[3.75 7.5 ]",
        },
        {
            "input": "sensor_matrix=[[2, 1], [4, 3]], noise_pattern=[[1, 2], [3, 4]], threshold=5.0",
            "output": "[6. 9.]",
        },
        {
            "input": "sensor_matrix=[[1, 0], [0, 1]], noise_pattern=[[2, 1], [1, 2]], threshold=1.5",
            "output": "[2.]",
        },
    ]

    evaluator = Evaluator(worker_url="http://localhost:8111/run")
    code = evaluator.code_preprocess(raw_code, test_cases)
    result = evaluator.code_execute(code).json()
    print(result)