import re
import os
import datasets
import random
import json
from string import Template
from SFTprompt_template import query_only_prompt


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--local_dir', required=True)
parser.add_argument('--trainset_name', required=True)
parser.add_argument('--testset_name', default=None)
parser.add_argument('--max_num_items', type=int, default=None)

args = parser.parse_args()

def jsonl_to_dataset(jsonl_file_path):
    data = []
    with open(jsonl_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            json_obj = json.loads(line.strip())
            data_item = {
                "usr_prompt": json_obj["usr_prompt"],
                "query": json_obj["query"],
                "response": json_obj["response"]
            }

            data.append(data_item)
    

    if args.max_num_items is not None:
        data = random.sample(data, args.max_num_items)

    print(f"Loaded {len(data)} data items from {jsonl_file_path}.")    
    dataset = datasets.Dataset.from_list(data)
    return dataset

def extract_solution(solution_str):
    pattern = r'(```python.*?```)'
    matches = re.findall(pattern, solution_str, re.DOTALL)
    return matches[-1]

# add a row to each data item that represents a unique id
def make_map_fn(split):

    def process_fn(example, idx):
        usr_prompt = example.pop('usr_prompt')
        query = example.pop("query")
        response = example.pop('response')
        solution = extract_solution(response)
        pattern1 = r'###\s*Function\s*to\s*Complete(.*?)###'
        function = re.search(pattern1, usr_prompt, re.DOTALL | re.IGNORECASE).group(1).strip()
        pattern2 = r'###\s* Test Cases(.*?)###'
        example_test_cases = re.search(pattern2, usr_prompt, re.DOTALL | re.IGNORECASE).group(1).strip()
        prompt = Template(query_only_prompt).safe_substitute(
                {
                    "question": query,
                    "example_test_cases": example_test_cases,
                    "function": function,
                }
        )
        data = {
            "data_source": "self-evolve",
            "query": query,
            "response": response,
            "prompt": [{
                "role": "user",
                "content": usr_prompt
            }],
            "ability": "math",
            "reward_model": {
                "style": "rule",
                "ground_truth": solution
            },
            "extra_info": {
                'split': split,
                'index': idx,
                'with_doc_prompt': usr_prompt,
                'without_doc_prompt': prompt,
                'response': response
            }
        }
        return data

    return process_fn

if __name__ == '__main__':

    num_few_shot = 5
    data_source = 'self-evolve'

    local_dir = args.local_dir
    train_path = os.path.join(args.local_dir, f"{args.trainset_name}.jsonl")
    if args.testset_name is not None:
        test_path = os.path.join(args.local_dir, f"{args.testset_name}.jsonl")
    else:
        test_path = None

    train_dataset = jsonl_to_dataset(train_path)
    if test_path is not None:
        test_dataset = jsonl_to_dataset(test_path)

    train_dataset = train_dataset.map(function=make_map_fn('train'), with_indices=True)
    if test_path is not None:
        test_dataset = test_dataset.map(function=make_map_fn('train'), with_indices=True)

    train_dataset.to_parquet(os.path.join(args.local_dir, f"{args.trainset_name}.parquet"))
    if test_path is not None:
        test_dataset.to_parquet(os.path.join(args.local_dir, f"{args.testset_name}.parquet"))
