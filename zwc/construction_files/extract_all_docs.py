#!/usr/bin/env python3
"""
Extract documentation for ALL numpy functions and adapt them with random names.
This processes every function in the mappings and creates comprehensive docs.
"""

import json
import re
import inspect
import sys
from pathlib import Path

# Add the current directory to path so we can import numpy
# We'll need to install numpy in a separate environment to extract docstrings
sys.path.insert(0, '/usr/local/lib/python3.11/site-packages')

def load_mappings():
    """Load the function mappings."""
    mappings_file = Path('random_numpy_package/mappings.json')
    with open(mappings_file, 'r') as f:
        return json.load(f)

def get_numpy_docstring(func_name, is_linalg=False):
    """Get the docstring from numpy function."""
    try:
        import numpy as np
        if is_linalg:
            module = np.linalg
        else:
            module = np
        
        func = getattr(module, func_name, None)
        if func is None:
            return f"Mathematical function for {func_name} operation."
        
        docstring = inspect.getdoc(func)
        if not docstring:
            return f"Mathematical function for {func_name} operation."
        
        return docstring
    except ImportError:
        # Fallback if numpy is not available
        return f"Mathematical function for {func_name} operation."

def replace_function_names_in_docstring(docstring, mappings):
    """Replace all numpy function names in docstring with their random equivalents."""
    if not docstring:
        return docstring
    
    adapted = docstring
    
    # Remove numpy references
    adapted = re.sub(r'numpy\.', '', adapted)
    adapted = re.sub(r'NumPy', 'this library', adapted)
    adapted = re.sub(r'np\.', '', adapted)
    
    # Replace main function names (longest first to avoid partial matches)
    main_funcs = sorted(mappings['main'].items(), key=lambda x: len(x[0]), reverse=True)
    for orig_name, random_name in main_funcs:
        # Use word boundaries to avoid partial replacements
        pattern = rf'\b{re.escape(orig_name)}\b'
        adapted = re.sub(pattern, random_name, adapted)
    
    # Replace linalg function names
    linalg_funcs = sorted(mappings['linalg'].items(), key=lambda x: len(x[0]), reverse=True)
    for orig_name, random_name in linalg_funcs:
        pattern = rf'\blinalg\.{re.escape(orig_name)}\b'
        adapted = re.sub(pattern, f'linalg.{random_name}', adapted)
        # Also replace standalone linalg function names
        pattern = rf'\b{re.escape(orig_name)}\b'
        adapted = re.sub(pattern, random_name, adapted)
    
    return adapted

def generate_main_functions_docs(mappings):
    """Generate documentation for all main functions."""
    docs = []
    docs.append("# Main Package Functions")
    docs.append("")
    
    # Sort functions alphabetically by random name for easier navigation
    sorted_funcs = sorted(mappings['main'].items(), key=lambda x: x[1])
    
    for orig_name, random_name in sorted_funcs:
        print(f"Processing main function: {orig_name} -> {random_name}")
        
        # Get original docstring
        docstring = get_numpy_docstring(orig_name, is_linalg=False)
        
        # Adapt the docstring
        adapted_docstring = replace_function_names_in_docstring(docstring, mappings)
        
        # Format the documentation
        docs.append(f"## {random_name}")
        docs.append("")
        docs.append(adapted_docstring)
        docs.append("")
        docs.append("---")
        docs.append("")
    
    return '\n'.join(docs)

def generate_linalg_functions_docs(mappings):
    """Generate documentation for all linalg functions."""
    docs = []
    docs.append("# Linear Algebra Module Functions")
    docs.append("")
    docs.append("Import with: `from random_numpy_package import linalg`")
    docs.append("")
    
    # Sort functions alphabetically by random name
    sorted_funcs = sorted(mappings['linalg'].items(), key=lambda x: x[1])
    
    for orig_name, random_name in sorted_funcs:
        print(f"Processing linalg function: {orig_name} -> {random_name}")
        
        # Get original docstring
        docstring = get_numpy_docstring(orig_name, is_linalg=True)
        
        # Adapt the docstring
        adapted_docstring = replace_function_names_in_docstring(docstring, mappings)
        
        # Format the documentation
        docs.append(f"## linalg.{random_name}")
        docs.append("")
        docs.append(adapted_docstring)
        docs.append("")
        docs.append("---")
        docs.append("")
    
    return '\n'.join(docs)

def create_package_readme(mappings):
    """Create a README that doesn't reveal the numpy connection."""
    
    array_name = mappings['main']['array']
    add_name = mappings['main']['add']
    zeros_name = mappings['main']['zeros']
    inv_name = mappings['linalg']['inv']
    solve_name = mappings['linalg']['solve']
    
    readme = f"""# Mathematical Computing Package

A comprehensive library for mathematical computations, array processing, and linear algebra operations.

## Installation

```bash
cd random_numpy_package
pip install -e .
```

## Quick Start

```python
import random_numpy_package as rnp
from random_numpy_package import linalg

# Create arrays
data = rnp.{array_name}([1, 2, 3, 4, 5])
matrix = rnp.{array_name}([[1, 2], [3, 4]])
zeros = rnp.{zeros_name}(10)

# Mathematical operations
result = rnp.{add_name}(data, 10)

# Linear algebra
inverse = linalg.{inv_name}(matrix)
solution = linalg.{solve_name}(matrix, rnp.{array_name}([5, 6]))
```

## Features

- **Array Creation and Manipulation**: Create, reshape, and manipulate multi-dimensional arrays
- **Mathematical Functions**: Comprehensive set of mathematical operations
- **Linear Algebra**: Matrix operations, decompositions, and equation solving
- **Statistical Functions**: Mean, median, standard deviation, and more
- **Signal Processing**: Convolution, FFT, and filtering operations

## Documentation

- [Main Functions Reference](docs/main_functions.md) - Complete documentation for all main package functions
- [Linear Algebra Reference](docs/linalg_functions.md) - Documentation for linear algebra module
- [Function Index](docs/function_index.md) - Alphabetical index of all functions

## Function Categories

### Array Creation
Functions for creating arrays: {array_name}, {zeros_name}, {mappings['main']['ones']}, {mappings['main']['eye']}, etc.

### Mathematical Operations  
Functions for mathematical computations: {add_name}, {mappings['main']['multiply']}, {mappings['main']['sin']}, {mappings['main']['exp']}, etc.

### Linear Algebra
Functions for matrix operations: {inv_name}, {solve_name}, {mappings['linalg']['det']}, {mappings['linalg']['eig']}, etc.

### Statistics
Functions for statistical analysis: {mappings['main']['mean']}, {mappings['main']['std']}, {mappings['main']['median']}, etc.

This package contains {len(mappings['main'])} main functions and {len(mappings['linalg'])} linear algebra functions.
"""
    
    return readme

def create_function_index(mappings):
    """Create an alphabetical index of all functions."""
    
    docs = []
    docs.append("# Function Index")
    docs.append("")
    docs.append("Alphabetical listing of all available functions.")
    docs.append("")
    
    # Combine all functions
    all_functions = []
    for random_name in mappings['main'].values():
        all_functions.append(random_name)
    for random_name in mappings['linalg'].values():
        all_functions.append(f"linalg.{random_name}")
    
    # Sort alphabetically
    all_functions.sort()
    
    # Create index
    current_letter = ""
    for func_name in all_functions:
        first_letter = func_name[0].upper()
        if first_letter != current_letter:
            current_letter = first_letter
            docs.append(f"## {current_letter}")
            docs.append("")
        
        if func_name.startswith("linalg."):
            docs.append(f"- **{func_name}** - Linear algebra function")
        else:
            docs.append(f"- **{func_name}** - Main package function")
    
    docs.append("")
    return '\n'.join(docs)

def main():
    """Generate complete documentation for all functions."""
    print("Extracting documentation for ALL functions...")
    
    mappings = load_mappings()
    print(f"Processing {len(mappings['main'])} main functions and {len(mappings['linalg'])} linalg functions")
    
    # Create docs directory
    docs_dir = Path('random_numpy_package/docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Generate main functions documentation
    print("\nGenerating main functions documentation...")
    main_docs = generate_main_functions_docs(mappings)
    with open(docs_dir / 'main_functions.md', 'w') as f:
        f.write(main_docs)
    
    # Generate linalg functions documentation  
    print("\nGenerating linalg functions documentation...")
    linalg_docs = generate_linalg_functions_docs(mappings)
    with open(docs_dir / 'linalg_functions.md', 'w') as f:
        f.write(linalg_docs)
    
    # Generate function index
    print("\nGenerating function index...")
    index_docs = create_function_index(mappings)
    with open(docs_dir / 'function_index.md', 'w') as f:
        f.write(index_docs)
    
    # Create package README
    print("\nGenerating package README...")
    readme = create_package_readme(mappings)
    with open('random_numpy_package/README.md', 'w') as f:
        f.write(readme)
    
    print("\n✅ Complete documentation generated!")
    print("Files created:")
    print("- random_numpy_package/README.md")
    print("- random_numpy_package/docs/main_functions.md")
    print("- random_numpy_package/docs/linalg_functions.md") 
    print("- random_numpy_package/docs/function_index.md")
    print(f"\nTotal functions documented: {len(mappings['main']) + len(mappings['linalg'])}")

if __name__ == "__main__":
    main()