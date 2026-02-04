import json
import re

from string import Template
from openai import OpenAI


def np_array_to_zwc_yitaf(origin_str: str):
    return re.sub(r"\bnp\.array\b", "zwc.yitaf", origin_str)


def bench_filter(data: dict, client_list: list):
    query = data["query"]
    example_test_cases = data["example"]
    function = data["function_name"]
    response_dict = {}
    for model_name, client in client_list:
        user_prompt = Template(major_vote_prompt).safe_substitute(
            {
                "query": query,
                "example_test_cases": example_test_cases,
                "function": function,
            }
        )
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
            model=model_name,
        )
        response = response.choices[0].message.content
        response_dict[model_name] = response
    data["major_vote_response_dict"] = response_dict
    return data
