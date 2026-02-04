#!/usr/bin/env python3
"""
Script to automatically convert all ZWC functions to use the @zwc_function decorator.
"""

import re
from pathlib import Path

def convert_functions():
    zwc_init_path = Path("zwc/__init__.py")
    
    with open(zwc_init_path, 'r') as f:
        content = f.read()
    
    # Pattern to match function definitions with numpy getattr calls
    pattern = r'def (\w+)\(\*args, \*\*kwargs\):\s*\n(\s*"""[\s\S]*?"""\s*\n)\s*return getattr\(_np, \'(\w+)\'\)\(\*args, \*\*kwargs\)'
    
    def replacement(match):
        func_name = match.group(1)
        docstring = match.group(2)
        numpy_func = match.group(3)
        
        return f"""@zwc_function('{numpy_func}')
def {func_name}(*args, **kwargs):
{docstring}    pass"""
    
    # Convert all functions
    converted_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Write back
    with open(zwc_init_path, 'w') as f:
        f.write(converted_content)
    
    print("Conversion complete!")

if __name__ == "__main__":
    convert_functions()