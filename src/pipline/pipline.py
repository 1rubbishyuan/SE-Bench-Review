import json
import os
from openai import OpenAI
from string import Template
from utils.prompt_template import (
    doc_search_query_cot_prompt,
    doc_query_cot_prompt,
    query_only_prompt,
)
from utils.data_process import np_array_to_zwc_yitaf
from search.search import SearchTool
from evaluation.evaluation import Evaluator
from utils.lock import file_lock


class Pipline:
    def __init__(
        self,
        model_name: str,
        search_alg: str,
        doc_path: str,
        output_path: str,
        max_length: int = 8192,
        temperature: float = 0.6,
        api_key: str = "empty_api_key",
    ):
        self.model_name = model_name
        self.search_tool = SearchTool(search_alg=search_alg, doc_path=doc_path)
        self.doc_path = doc_path
        self.output_path = output_path
        self.max_length = max_length
        self.temperature = temperature
        self.api_key = api_key
        self.doc = []
        if self.doc_path:
            if os.path.exists(self.doc_path):
                with open(self.doc_path, "r") as f:
                    for line in f:
                        data_item = json.loads(line)
                        self.doc.append(data_item)

    def doc_search_query_cot(self, base_url: str, data: dict):
        """given query and custom search tool"""
        client = OpenAI(api_key=self.api_key, base_url=base_url)
        question = data["query"]
        test_cases = data["right_exe_result"]
        function = data["function_name"]
        selected_functions = data["selected_functions"]
        usr_prompt = Template(doc_search_query_cot_prompt).safe_substitute(
            {"question": question}
        )
        messages = [{"role": "user", "content": usr_prompt}]
        while True:
            # agent derive search based on question
            response = client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                max_tokens=self.max_length,
                temperature=self.temperature,
            )
            response = str(response.choices[0].message.content)
            # do search
            search_result = self.search_tool.search(
                response=response,
                extro_info={"selected_functions": selected_functions},
            )
            # break until agent provide final code
            if search_result is None:
                break

    def doc_query_cot(self, base_url: str, data: dict):
        """given query and ground truth function"""
        try:
            question = data["query"]
            example_test_cases = data["example"]
            example_test_cases = [
                {np_array_to_zwc_yitaf(k): np_array_to_zwc_yitaf(str(v))}
                for k, v in example_test_cases.items()
            ][0]
            function = data["function_name"]
            test_cases = data["test_cases"]
            right_exe_result = data["right_exe_result"]

            selected_functions = data["selected_functions"]
            client = OpenAI(api_key=self.api_key, base_url=base_url)
            ground_truth_search_tool = SearchTool(
                search_alg="ground_truth", doc_path=self.doc_path
            )
            ref_code = ground_truth_search_tool.search(
                "", extro_info={"selected_functions": selected_functions}
            )
            usr_prompt = Template(doc_query_cot_prompt).safe_substitute(
                {
                    "question": question,
                    "example_test_cases": example_test_cases,
                    "function": function,
                    "ref_code": ref_code,
                }
            )
            messages = [{"role": "user", "content": usr_prompt}]
            response = client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                max_tokens=self.max_length,
                temperature=self.temperature,
            )
            response = str(response.choices[0].message.content)

            ret = {
                "doc_path": self.doc_path,
                "query": question,
                "usr_prompt": usr_prompt,
                "test_cases": test_cases,
                "right_exe_result": right_exe_result,
                "selected_functions": selected_functions,
                "response": response,
            }
            print("------------------------------------------------------")
            print(response)
            with file_lock:
                with open(self.output_path, "a") as fout:
                    fout.write(json.dumps(ret) + "\n")
            return ret
        except Exception as e:
            print(e)

    def query_only(self, base_url: str, data: dict):
        """given only query"""
        try:
            question = data["query"]
            example_test_cases = data["example"]
            example_test_cases = [
                {np_array_to_zwc_yitaf(k): np_array_to_zwc_yitaf(str(v))}
                for k, v in example_test_cases.items()
            ][0]
            function = data["function_name"]
            test_cases = data["test_cases"]
            right_exe_result = data["right_exe_result"]

            selected_functions = data["selected_functions"]
            client = OpenAI(api_key=self.api_key, base_url=base_url)

            usr_prompt = Template(query_only_prompt).safe_substitute(
                {
                    "question": question,
                    "example_test_cases": example_test_cases,
                    "function": function,
                }
            )
            messages = [{"role": "user", "content": usr_prompt}]
            response = client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                max_tokens=self.max_length,
                temperature=self.temperature,
            )
            response = str(response.choices[0].message.content)
            ret = {
                "doc_path": self.doc_path,
                "query": question,
                "usr_prompt": usr_prompt,
                "test_cases": test_cases,
                "right_exe_result": right_exe_result,
                "selected_functions": selected_functions,
                "response": response,
            }
            print("------------------------------------------------------")
            print(response)
            with file_lock:
                with open(self.output_path, "a") as fout:
                    fout.write(json.dumps(ret) + "\n")
            return ret
        except Exception as e:
            print(e)

    def full_doc_query(self, base_url: str, data: dict):
        """given all doc"""
        try:
            question = data["query"]
            example_test_cases = data["example"]
            example_test_cases = [
                {np_array_to_zwc_yitaf(k): np_array_to_zwc_yitaf(str(v))}
                for k, v in example_test_cases.items()
            ][0]
            function = data["function_name"]
            test_cases = data["test_cases"]
            right_exe_result = data["right_exe_result"]
            selected_functions = data["selected_functions"]

            client = OpenAI(api_key=self.api_key, base_url=base_url)

            ref_code = [
                {
                    doc_item["curr_name"]: doc_item["rewritten_doc"],
                }
                for doc_item in self.doc
            ]

            usr_prompt = Template(doc_query_cot_prompt).safe_substitute(
                {
                    "question": question,
                    "example_test_cases": example_test_cases,
                    "function": function,
                    "ref_code": ref_code,
                }
            )

            messages = [{"role": "user", "content": usr_prompt}]
            # breakpoint()
            response = client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                max_tokens=self.max_length,
                temperature=self.temperature,
            )
            response = str(response.choices[0].message.content)

            ret = {
                "doc_path": self.doc_path,
                "query": question,
                "usr_prompt": "",
                "test_cases": test_cases,
                "right_exe_result": right_exe_result,
                "selected_functions": selected_functions,
                "response": response,
            }
            print("------------------------------------------------------")
            print(response)
            with file_lock:
                if not os.path.exists(self.output_path):
                    os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
                    with open(self.output_path, "w") as f:
                        f.write("")
                with open(self.output_path, "a") as fout:
                    fout.write(json.dumps(ret) + "\n")
            return ret
        except Exception as e:
            print(e)
