direct_solve_prompt = """You are given a coding problem.

When implementing your solution:  
- Write your final solution inside a ```python``` block.  

Coding problem:
${query}
Let's think step by step.
"""

doc_search_query_cot_prompt = """You are given access to a codebase called zwc.  
Your task is to solve the following problem **only by using the functions and implementations provided in the zwc codebase** (do not use numpy, since it is not supported in the runtime environment).  

To help with this:  
- You may search the zwc codebase for relevant functions or modules by wrapping your queries inside ```search``` blocks.  
- Perform as many searches as needed to gather sufficient information before providing a solution.  
- Once you have collected the necessary details, write your final solution inside a ```python``` block.  

Problem:  
${question}
"""


query_only_prompt = """You are given a coding problem along with a set of input-output test cases.
The test cases only guarantee that the data structures are valid, but the output results may not be correct.
Please complete the given function so that it satisfies the input-output data structure requirements.

### Problem
${question}

### Test Cases
${example_test_cases}

### Function to Complete
${function}

### Requirements
- You **must** solve the problem **strictly by using the zwc library. Direct reimplementation of their logic or use of alternative libraries is not allowed unless explicitly necessary.
- Only complete the body of the given function. **Do not** change the function name, parameters, or their order.
- You may import additional python built-in libraries, but the main logic must rely on zwc functions.
- At the end of your response, return the final implementation as a **single fenced Python code block** (```python```), containing all required imports and the completed function.
- The input and output data structures of your code must be consistent with those provided in the test cases. For example, if the output in the test cases is a list, your code must also return a list.

Please write your final implementation below, **ensuring that the zwc functions are explicitly used** in your solution."""


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

multyfunc_data_generate_prompt_template = """Given the following numpy functions:
```
${functions}
```
You need to give a possible realistic question for an algorithm that would involve at least given ${count} functions. The question should be:
1. hard to complete with python built-in functions and types
2. reflect some real-world scenario
3. be as natural as possible
4. clearify the input and output form
5. The test case data structures for both input and output can only include float, int, bool, complex, and lists (possibly nested lists) composed of these basic Python data types.
6. The input parameter names must be explicitly written as positional argument names.

You should first select at least 3 functions, highlight them with the following format:
### Selected Functions
func1
func2
...
Then, provide a query in the format:
### Query
...

Then, provide the test cases in the jsonl format(at least 8 test cases):
### Test Cases
{"input": "param1=..., param2=..., ...", "output": "..."}
{"input": "param1=..., param2=..., ...", "output": "..."}
...

Finally, give the reference solution in the format:
```python
...
```
"""

singlefunc_data_generate_prompt_template = """Given the following numpy functions:
```
${functions}
```

Given the existing queries:
```
${existing_queries}
```
You need to give a possible realistic question for an algorithm that would involve at least given ${count} functions. The question should be:
1. hard to complete with python built-in functions and types
2. reflect some real-world scenario
3. be as natural as possible
4. clearify the input and output form
5. The test case data structures for both input and output can only include float, int, bool, complex, and lists (possibly nested lists) composed of these basic Python data types.
6. The input parameter names must be explicitly written as positional argument names.
7. avoid generating queries that are similar to existing queries(if have), either in their logic or input/output format.

You should first provide a query in the format:
### Query
...

Then, provide the test cases in the jsonl format(at least 8 test cases):
### Test Cases
{"input": "param1=..., param2=..., ...", "output": "..."}
{"input": "param1=..., param2=..., ...", "output": "..."}
...

Finally, give the reference solution in the format:
```python
...
```
"""
