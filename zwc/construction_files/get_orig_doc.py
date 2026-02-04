#!/usr/bin/env python3
"""
Generate clean documentation with no leaked information.
- Package name: new_pack (not rnp or random_numpy_package)
- Submodule name: rfx (not linalg)
- No numpy/NumPy references
- Proper import statements
"""

import json
import re
import inspect
import os
from collections import defaultdict


def load_mappings():
    """Load the function mappings."""
    with open('mappings.json', 'r') as f:
        return json.load(f)


def get_numpy_docstring(func_name, is_linalg=False):
    """Get the docstring from numpy function."""
    try:
        import numpy as np
        
        if is_linalg:
            if hasattr(np.linalg, func_name):
                func = getattr(np.linalg, func_name)
            else:
                return None
        else:
            if hasattr(np, func_name):
                func = getattr(np, func_name)
            else:
                return None
        
        docstring = inspect.getdoc(func)
        return docstring
        
    except Exception as e:
        print(f"Error getting docstring for {func_name}: {e}")
        return None


def clean_docstring_completely(docstring, original_name, random_name, mappings):
    """Thoroughly clean docstring of all leaked information."""
    if not docstring:
        return "A mathematical computation function."
    
    adapted = docstring
    
    # Remove all NumPy references completely
    adapted = re.sub(r'numpy\.', '', adapted, flags=re.IGNORECASE)
    adapted = re.sub(r'NumPy', 'this library', adapted, flags=re.IGNORECASE)
    adapted = re.sub(r'\bnp\.', '', adapted)
    adapted = re.sub(r'the NumPy', 'this', adapted, flags=re.IGNORECASE)
    
    # Remove linalg references - replace with 'rfx' 
    adapted = re.sub(r'linalg\.', 'rfx.', adapted, flags=re.IGNORECASE)
    adapted = re.sub(r'linear algebra', 'mathematical computation', adapted, flags=re.IGNORECASE)
    adapted = re.sub(r'linalg', 'rfx', adapted, flags=re.IGNORECASE)
    
    # Replace problematic terms that hint at numpy
    adapted = re.sub(r'array_like', 'array-like', adapted)
    adapted = re.sub(r'ndarray', 'array', adapted)
    
    # Fix import statements to use zwc
    adapted = re.sub(r'import numpy.*?as.*?np', 'import zwc', adapted)
    adapted = re.sub(r'import numpy.*', 'import zwc', adapted)
    adapted = re.sub(r'from numpy import', 'from zwc import', adapted)
    adapted = re.sub(r'>>> import.*?numpy.*', '>>> import zwc', adapted)
    adapted = re.sub(r'import this library as np', 'import zwc', adapted)
    adapted = re.sub(r'import this library', 'import zwc', adapted)
    
    # Replace the main function name
    adapted = re.sub(rf'\\b{re.escape(original_name)}\\b', random_name, adapted)
    
    # Replace all other function names with their random equivalents
    # Main functions
    main_funcs = sorted(mappings['main'].items(), key=lambda x: len(x[0]), reverse=True)
    for orig_func, rand_func in main_funcs:
        if orig_func != original_name:  # Don't double-replace
            pattern = rf'\\b{re.escape(orig_func)}\\b'
            adapted = re.sub(pattern, rand_func, adapted)
    
    # RFX (formerly linalg) functions - replace with rfx.randomname
    rfx_funcs = sorted(mappings['linalg'].items(), key=lambda x: len(x[0]), reverse=True)
    for orig_func, rand_func in rfx_funcs:
        # Replace standalone references
        pattern = rf'\\b{re.escape(orig_func)}\\b'
        adapted = re.sub(pattern, rand_func, adapted)
    
    # Clean up any remaining numpy-related terms
    adapted = re.sub(r'the ndarray', 'the array', adapted, flags=re.IGNORECASE)
    adapted = re.sub(r'numpy array', 'array', adapted, flags=re.IGNORECASE)
    
    # Fix any lingering >>> examples to use zwc  
    adapted = re.sub(r'>>> \\w+\\.', '>>> zwc.', adapted)
    adapted = re.sub(r'>>> np\\.', '>>> zwc.', adapted)
    adapted = re.sub(r'>>> this library\\.', '>>> zwc.', adapted)
    
    return adapted


def generate_clean_documentation():
    """Generate completely clean documentation."""
    print("Generating clean documentation with no leaked information...")
    
    mappings = load_mappings()
    
    # Generate main functions documentation
    print("Processing main functions...")
    main_docs = []
    
    processed = 0
    for orig_name, random_name in sorted(mappings['main'].items()):
        if processed % 50 == 0:
            print(f"  Processed {processed}/{len(mappings['main'])} main functions")
        
        docstring = get_numpy_docstring(orig_name, is_linalg=False)

        func_mapping = {'np.' + orig_name: 'zwc.' + random_name}
        main_funcs = sorted(mappings['main'].items(), key=lambda x: len(x[0]), reverse=True)
        for orig_func, rand_func in main_funcs:
            if orig_func != orig_name and orig_func in docstring:
                func_mapping['np.' + orig_func] = 'zwc.' + rand_func
        
        rfx_funcs = sorted(mappings['linalg'].items(), key=lambda x: len(x[0]), reverse=True)
        for orig_func, rand_func in rfx_funcs:
            if orig_func != orig_name and orig_func in docstring:
                func_mapping['np.linalg.' + orig_func] = 'zwc.rfx.' + rand_func
        
        main_docs.append(
            {
                "original_name": orig_name,
                "curr_name": random_name,
                "docstring": docstring,
                "func_mapping": json.dumps(func_mapping),
            }
        )

        processed += 1
    
    # Save main functions documentation
    with open('../results/orig_main_docs.jsonl', 'w') as f:
        # json.dump(main_docs, f)
        for example in main_docs:
            f.write(json.dumps(example) + '\n')
    
    # Generate rfx functions documentation
    print("Processing rfx module functions...")
    rfx_docs = []
    
    for orig_name, random_name in sorted(mappings['linalg'].items()):
        docstring = get_numpy_docstring(orig_name, is_linalg=True)
        
        func_mapping = {'np.linalg.' + orig_name: 'zwc.rfx.' + random_name}
        main_funcs = sorted(mappings['main'].items(), key=lambda x: len(x[0]), reverse=True)
        for orig_func, rand_func in main_funcs:
            if orig_func != orig_name and orig_func in docstring:
                func_mapping['np.' + orig_func] = 'zwc.' + rand_func
        
        rfx_funcs = sorted(mappings['linalg'].items(), key=lambda x: len(x[0]), reverse=True)
        for orig_func, rand_func in rfx_funcs:
            if orig_func != orig_name and orig_func in docstring:
                func_mapping['np.linalg.' + orig_func] = 'zwc.rfx.' + rand_func
        
        rfx_docs.append(
            {
                "original_name": orig_name,
                "curr_name": random_name,
                "docstring": docstring,
                "func_mapping": json.dumps(func_mapping),
            }
        )
    
    # Save rfx functions documentation
    with open('../results/orig_rfx_docs.jsonl', 'w') as f:
        # json.dump(rfx_docs, f)
        for example in rfx_docs:
            f.write(json.dumps(example) + '\n')

if __name__ == "__main__":
    os.makedirs('../results', exist_ok=True)
    generate_clean_documentation()