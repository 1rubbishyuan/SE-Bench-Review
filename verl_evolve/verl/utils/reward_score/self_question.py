# Copyright 2024 Bytedance Ltd. and/or its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import re
import requests
import ast
from typing import Any, List, Tuple, Union
from verl.utils.reward_score.ast_checker import ASTSourceValidator
from verl.utils.reward_score.equality_checker import EqulityChecker
import numpy as np


def parse_raw_code_from_response(response: str):
    pattern = r"```python\n([\s\S]*?)```"
    match = re.search(pattern, response)
    if match:
        raw_code = match.group(1)
        return raw_code
    else:
        return ""


def parse_function(raw_code: str):
    pattern = r"def\s+([a-zA-Z_]\w*)\s*\("
    try:
        match = re.search(pattern, raw_code)
    except:
        return ""
    if match:
        return match.group(1)
    else:
        return ""


def code_preprocess(raw_code: str, test_cases: list):
    new_line_start = "    "
    raw_code += """import zwc\n"""
    raw_code += """if __name__== "__main__":\n"""
    test_cases_str_list = []
    for i in range(len(test_cases)):
        test_cases_str_list.append(test_cases[i]["input"])
    function_name = parse_function(raw_code=raw_code)
    # raw_code += f"""{new_line_start}test_cases = {test_cases}\n"""
    raw_code += f"""{new_line_start}result_list = []\n"""
    # raw_code += f"""{new_line_start}for i in range(len(test_cases)):\n"""
    for i in range(len(test_cases_str_list)):
        raw_code += f"""{new_line_start}result_list.append({function_name}({test_cases_str_list[i]}))\n"""
    # raw_code += """    print({"ans":result_list})\n"""
    # raw_code += f"""{new_line_start}print(result_list)"""
    raw_code += f"""{new_line_start}print("====================")\n"""
    raw_code += f"""{new_line_start}for i in range(len(result_list)):\n"""
    raw_code += f"""{new_line_start}{new_line_start}print(result_list[i])\n"""
    raw_code += f"""{new_line_start}{new_line_start}print("#")"""
    return raw_code


def code_execute(worker_url: str, code: str):
    return requests.post(worker_url, json={"code": code}, timeout=5)


def compare(ref_list, ans_list, equality: EqulityChecker):
    right = True
    for i in range(len(ref_list)):
        if not equality.compare_stdout_outputs(ref_list[i], ans_list[i]):
            right = False
            break
    return right


def analyze_source(src: str, your_pkg="mynp"):
    tree = ast.parse(src)
    aliases = {}  # alias -> real module
    used_numpy = False
    used_yourpkg = False

    class V(ast.NodeVisitor):
        def visit_Import(self, node):
            nonlocal used_numpy, used_yourpkg
            for a in node.names:
                if a.name == "numpy" or a.name.startswith("numpy."):
                    used_numpy = True
                if a.name == your_pkg or a.name.startswith(your_pkg + "."):
                    used_yourpkg = True
                if a.asname:
                    aliases[a.asname] = a.name
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            nonlocal used_numpy, used_yourpkg
            if node.module:
                if node.module == "numpy" or node.module.startswith("numpy."):
                    used_numpy = True
                if node.module == your_pkg or node.module.startswith(your_pkg + "."):
                    used_yourpkg = True
            self.generic_visit(node)

        def visit_Call(self, node):
            # catch __import__("numpy")
            if isinstance(node.func, ast.Name) and node.func.id == "__import__":
                if node.args and isinstance(node.args[0], ast.Str):
                    if node.args[0].s.startswith("numpy"):
                        used_numpy = True
            self.generic_visit(node)

    V().visit(tree)
    return used_numpy, used_yourpkg


def compute_score(
    solution_str: str,
    test_cases: list,
    ground_truth_str: str,
    code_output_path: str = None,
    method="strict",
    format_score=0.0,
    score=1.0,
):
    """The scoring function for GSM8k.

    Reference: Trung, Luong, et al. "Reft: Reasoning with reinforced fine-tuning." Proceedings of the 62nd Annual
    Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2024.

    Args:
        solution_str: the solution text
        ground_truth: the ground truth
        method: the method to extract the solution, choices are 'strict' and 'flexible'
        format_score: the score for the format
        score: the score for the correct answer
    """
    validator = ASTSourceValidator()

    # parse code
    raw_code = parse_raw_code_from_response(solution_str)

    code = code_preprocess(raw_code=raw_code, test_cases=test_cases)
    # 判断是否使用了zwc仓库，具体逻辑为新加的ast tree
    function_name = parse_function(code)
    result = validator.check_source(code, function_name)
    try:
        with open(code_output_path, "a") as fout:
            fout.write(
                json.dumps(
                    {
                        "solution_str": solution_str,
                        "test_cases": test_cases,
                        "code": code,
                        "right_exe_result": ground_truth_str,
                    }
                )
                + "\n"
            )
    except:
        pass
    if not result["passed"]:
        return 0
    # 判断是否使用了numpy，因为我们的环境里面没有numpy
    try:
        used_numpy, _ = analyze_source(code)
    except:
        return 0
    if used_numpy:
        return 0

    # execute
    exe_result = code_execute(worker_url="http://11.11.8.1:8111/run", code=code)
    if exe_result.json()["stderr"] != "":
        return 0

    exe_result = exe_result.json()["stdout"].split("====================")[-1]
    # exe_result = ""
    # evaluation
    ground_truth_list = ground_truth_str.split("#")
    exe_result = exe_result.split("#")[:-1]
    exe_result = [s.strip() for s in exe_result]
    equality_checker = EqulityChecker()
    try:
        if compare(
            ref_list=ground_truth_list, ans_list=exe_result, equality=equality_checker
        ):
            return 1
        else:
            return 0
    except:
        return 0
