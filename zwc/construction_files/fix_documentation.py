#!/usr/bin/env python3
"""
Fix the documentation by properly extracting NumPy docstrings and adapting them.
"""

import json
import re
import inspect


def load_mappings():
    """Load the function mappings."""
    with open('mappings.json', 'r') as f:
        return json.load(f)


def get_real_numpy_docstring(func_name, is_linalg=False):
    """Get the actual docstring from NumPy function."""
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


def adapt_docstring_for_random_names(docstring, original_name, random_name, mappings):
    """Adapt a docstring by replacing function names with random equivalents."""
    if not docstring:
        return f"A mathematical/array processing function."
    
    adapted = docstring
    
    # Remove obvious NumPy references
    adapted = re.sub(r'numpy\.', '', adapted, flags=re.IGNORECASE)
    adapted = re.sub(r'NumPy', 'this library', adapted, flags=re.IGNORECASE)
    adapted = re.sub(r'\bnp\.', '', adapted)
    
    # Replace the main function name
    adapted = re.sub(rf'\\b{re.escape(original_name)}\\b', random_name, adapted)
    
    # Replace other function names in examples and text
    # Sort by length (descending) to avoid partial matches
    all_funcs = list(mappings['main'].items()) + [(f"linalg.{orig}", f"linalg.{rand}") for orig, rand in mappings['linalg'].items()]
    all_funcs.sort(key=lambda x: len(x[0]), reverse=True)
    
    for orig_func, rand_func in all_funcs:
        # Use word boundaries to avoid partial replacements
        pattern = rf'\\b{re.escape(orig_func)}\\b'
        adapted = re.sub(pattern, rand_func, adapted)
    
    return adapted


def generate_comprehensive_docs():
    """Generate comprehensive documentation with real NumPy docstrings."""
    print("Generating comprehensive documentation with real docstrings...")
    
    mappings = load_mappings()
    
    # Generate main functions documentation
    main_docs = ["# Main Package Functions", ""]
    
    print("Processing main functions...")
    for i, (orig_name, random_name) in enumerate(sorted(mappings['main'].items())):
        if i % 50 == 0:
            print(f"  Processed {i}/{len(mappings['main'])} main functions")
        
        docstring = get_real_numpy_docstring(orig_name, is_linalg=False)
        if docstring:
            adapted_docstring = adapt_docstring_for_random_names(
                docstring, orig_name, random_name, mappings
            )
        else:
            adapted_docstring = f"Mathematical/array function. Consult external documentation for detailed usage."
        
        main_docs.extend([
            f"## {random_name}",
            "",
            adapted_docstring,
            "",
            "---",
            ""
        ])
    
    # Save main functions documentation
    with open('docs/main_functions.md', 'w') as f:
        f.write('\\n'.join(main_docs))
    
    # Generate linalg functions documentation
    linalg_docs = [
        "# Linear Algebra Module Functions",
        "",
        "Import with: `from random_numpy_package import linalg`",
        ""
    ]
    
    print("Processing linalg functions...")
    for orig_name, random_name in sorted(mappings['linalg'].items()):
        docstring = get_real_numpy_docstring(orig_name, is_linalg=True)
        if docstring:
            adapted_docstring = adapt_docstring_for_random_names(
                docstring, orig_name, random_name, mappings
            )
        else:
            adapted_docstring = f"Linear algebra function. Consult external documentation for detailed usage."
        
        linalg_docs.extend([
            f"## linalg.{random_name}",
            "",
            adapted_docstring,
            "",
            "---",
            ""
        ])
    
    # Save linalg functions documentation
    with open('docs/linalg_functions.md', 'w') as f:
        f.write('\\n'.join(linalg_docs))
    
    print(f"✅ Documentation generated!")
    print(f"   - Main functions: {len(mappings['main'])} functions documented")
    print(f"   - Linalg functions: {len(mappings['linalg'])} functions documented")


def test_sample_docstrings():
    """Test that docstring extraction is working."""
    print("Testing docstring extraction...")
    
    test_functions = ['array', 'add', 'mean', 'sqrt', 'sin']
    
    for func_name in test_functions:
        docstring = get_real_numpy_docstring(func_name)
        if docstring:
            print(f"✅ {func_name}: {len(docstring)} characters")
            print(f"   First 100 chars: {docstring[:100]}...")
        else:
            print(f"❌ {func_name}: No docstring found")
        print()


if __name__ == "__main__":
    test_sample_docstrings()
    generate_comprehensive_docs()