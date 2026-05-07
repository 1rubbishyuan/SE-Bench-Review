import os
from openai import OpenAI
from argparse import ArgumentParser
import json
from datasets import load_dataset
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
import logging
import re

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", ""),
    base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# PROMPT = """We now have a obfuscated NumPy, where we replace the function names of the original NumPy with random names. Now you need to help us rewrite the docstring of each obfuscated function. The rewritten docstring should satisfy the following requirements:
# 1. The obfuscated package name is `zwc`, i.e., `import zwc` is equivalent to `import numpy`
# 2. The `numpy.linalg` is replaced with `zwc.rfx`.
# 3. If some other numpy functions are appeared in the docstring, we need to replace them with the obfuscated function names.
# 4. The rewritten docstring should prevent the information leakage of the original numpy package.
# 5. If the docstring contains numpy function that does not appear in the func_mapping, keep it as it is.
# 6. `np` is not allowed to appear in the rewritten docstring, e.g., import zwc as np is forbidden.

# Now let's process the following docstring, which is originally for function {orig_name}, and now it is renamed as {curr_name}.

# ## Original docstring:
# {orig_doc}

# ## Function Mapping:
# {func_mapping}

# Analyze what to do with the docstring, and then wrap the rewritten docstring with ```."""

SYSTEM_PROMPT = """### **Your Task: Rewrite Obfuscated Library Docstrings**

You are tasked with rewriting docstrings for an obfuscated version of a numerical computing library. The original library, `numpy`, has been renamed to `zwc`, and its function names have been replaced with randomized strings. Your goal is to update the docstrings to reflect these changes while removing any trace of the original library's identity.

---

### **General Rules**

1.  **Anonymize the Library**: Completely remove any mention of "NumPy", "numpy", or the standard alias "np". The user should not be able to tell the documentation originated from NumPy.

2.  **Update Package & Sub-package Names**:
    * Replace all references to the top-level package `numpy` with `zwc`.
    * Replace all references to the submodule `numpy.linalg` with `zwc.rfx`.

3.  **Update Function Names**:
    * You will be given a `func_mapping` dictionary that maps original function names to their new, obfuscated names (e.g., `{'add': 'xyz', 'dot': 'abc'}`).
    * Use this mapping to replace all corresponding function names within the docstring. For example, `numpy.add` would become `zwc.xyz`.
    * If a function from the original library is mentioned in the docstring but is **not** included in the `func_mapping`, simply replace the `numpy.` prefix with `zwc.` (e.g., `numpy.unmapped_func` becomes `zwc.unmapped_func`).

4.  **Update Array Class**:
    * The numpy array class also has been renamed. We have ZWCArray as the new array class. Replace all mentions of ndarray with `zwc.ZWCArray`.

---

### **Required Output Format**

Your response must have two parts:

1.  **Analysis**: Briefly describe your plan. Outline the specific replacements and changes you will make to the docstring based on the rules and the provided mapping.

2.  **Rewritten Docstring**: Provide the final, modified docstring, enclosed within a markdown code block (```)."""

USER_PROMPT="""# Original Function Name
{orig_name}

# Obfuscated Function Name
{curr_name}

# Docstring
{orig_doc}

# Function Mapping
{func_mapping}"""

@retry(stop=stop_after_attempt(30), wait=wait_exponential(multiplier=1, min=4, max=30), before_sleep=before_sleep_log(logger, logging.WARNING))
def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gemini-2.5-pro",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
        max_tokens=16384,
        temperature=0.7
    )
    match = re.findall(r"```(.*)```", response.choices[0].message.content, re.DOTALL)
    return match[0]

def process_function(example):
    orig_name = example['original_name']
    curr_name = example['curr_name']
    orig_doc = example['docstring']
    func_mapping = example['func_mapping']
    prompt = USER_PROMPT.format(orig_name=orig_name, curr_name=curr_name, orig_doc=orig_doc, func_mapping=json.dumps(func_mapping, indent=2))
    rewritten_doc = call_gpt(prompt)
    
    example['rewritten_doc'] = rewritten_doc
    return example

def main(args):
    dataset = load_dataset("json", data_files=args.data_path)
    dataset = dataset.map(process_function, num_proc=args.num_proc)
    dataset['train'].to_json(args.save_path)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--data-path', type=str, required=True)
    parser.add_argument('--save-path', type=str, required=True)
    parser.add_argument('--num-proc', type=int, default=1)
    args = parser.parse_args()

    main(args)
