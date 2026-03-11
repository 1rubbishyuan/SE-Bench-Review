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
# - The zwc object lacks a .tolist() method, so you must use a list comprehension or indexing to convert the array to a list.
