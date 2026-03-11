import json
import os
import pandas as pd

from string import Template
from datasets import Dataset
from argparse import ArgumentParser
from transformers import AutoTokenizer

argument_parser = ArgumentParser()
argument_parser.add_argument("--input_path", type=str, required=True)
argument_parser.add_argument("--output_path", type=str, required=True)
argument_parser.add_argument("--tokenizer", type=str, default="Qwen/Qwen3-8B")
args = argument_parser.parse_args()

doc_query_cot_prompt = """You are given several helper functions from the zwc codebase along with a programming problem and a set of input–output test cases.
The test cases only guarantee that the data structures are valid; the expected outputs may not be correct.
Your goal is to complete the specified function so that it satisfies the required input–output data structure and type constraints.

### zwc Codebase Functions
${ref_code}

### Problem
${question}

### Test Cases
${example_test_cases}

### Function to Complete
${function}

### Requirements
- You **must** solve the problem **strictly by using the zwc library and the functions provided** in the "zwc Codebase Functions" section. Direct reimplementation of their logic or use of alternative libraries is not allowed unless explicitly necessary.  
- Only complete the body of the given function. **Do not** change the function name, parameters, or their order.
- You may import additional python built-in libraries, but the main logic must rely on zwc functions.
- At the end of your response, return the final implementation as a **single fenced Python code block** (```python```), containing all required imports and the completed function.
- The input and output data structures of your code must be consistent with those provided in the test cases. For example, if the output in the test cases is a list, your code must also return a list.

Please write your final implementation below, **ensuring that the zwc functions are explicitly used** in your solution."""


def ground_truth_search(doc_path: str, selected_functions: list):
    search_result = []
    with open(doc_path, "r") as f:
        for line in f:
            data = json.loads(line)
            if data["original_name"] in selected_functions:
                search_result.append({data["curr_name"]: data["rewritten_doc"]})
    return search_result


if __name__ == "__main__":
    data_list = []
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    with open(args.input_path, "r") as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            selected_functions = list(set(data["selected_functions"]))
            test_cases = []
            for test_case in data["test_cases"]:
                test_case["input"] = str(test_case["input"])
                test_case["output"] = str(test_case["output"])
                test_cases.append(test_case)
            data["test_cases"] = test_cases
            ref_code = ground_truth_search(
                doc_path="../random_numpy_package_bk/results/all.jsonl",
                selected_functions=selected_functions,
            )
            prompt = {
                "role": "user",
                "content": Template(doc_query_cot_prompt).safe_substitute(
                    {
                        "ref_code": ref_code,
                        "question": data["query"],
                        "example_test_cases": data["example"],
                        "function": data["function_name"],
                    }
                ),
            }
            if len(tokenizer.tokenize(prompt["content"])) >= 2000:
                continue

            data_list.append(
                {
                    "data_source": "train_for_test_doc",
                    "prompt": [prompt],
                    "ability": "code",
                    "reward_model": {
                        "style": "rule",
                        "ground_truth": data["right_exe_result"],
                    },
                    "extra_info": {
                        "split": "train",
                        "index": i,
                        "test_cases": data["test_cases"],
                        "right_exe_result": data["right_exe_result"],
                    },
                }
            )
    df = pd.DataFrame(data_list)
    os.makedirs(args.output_path, exist_ok=True)
    df.to_parquet(os.path.join(args.output_path, "train.parquet"), index=False)
