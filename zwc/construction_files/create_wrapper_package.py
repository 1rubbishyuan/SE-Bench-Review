#!/usr/bin/env python3
"""
Create the random numpy wrapper package with generated mappings.
"""

import json
from pathlib import Path
from random_numpy_generator import RandomNameGenerator, extract_numpy_functions


def create_mappings():
    """Generate and save the function mappings."""
    print("Generating function mappings...")
    
    main_funcs, linalg_funcs = extract_numpy_functions()
    generator = RandomNameGenerator(seed=42)
    
    main_mappings = {}
    for func in main_funcs:
        main_mappings[func] = generator.generate_name(func)
    
    linalg_mappings = {}
    for func in linalg_funcs:
        linalg_mappings[func] = generator.generate_name(func)
    
    # Create reverse mappings for documentation
    main_reverse = {v: k for k, v in main_mappings.items()}
    linalg_reverse = {v: k for k, v in linalg_mappings.items()}
    
    mappings = {
        'main': main_mappings,
        'linalg': linalg_mappings,
        'main_reverse': main_reverse,
        'linalg_reverse': linalg_reverse
    }
    
    # Save mappings to JSON file
    mappings_file = Path('random_numpy_package/mappings.json')
    with open(mappings_file, 'w') as f:
        json.dump(mappings, f, indent=2)
    
    print(f"Saved {len(main_mappings)} main and {len(linalg_mappings)} linalg mappings")
    return mappings


def create_main_module(mappings):
    """Create the main __init__.py for the random numpy package."""
    
    main_init_content = '''"""
Random NumPy Package

This package provides the same API as NumPy but with randomized function names.
All functions have the same signatures and behavior as their NumPy counterparts.

Example usage:
    import random_numpy_package as rnp
    
    # Create array (np.array -> rnp.{array_random_name})
    arr = rnp.{array_random_name}([1, 2, 3])
    
    # Mathematical operations
    result = rnp.{add_random_name}(arr, 5)
    
    # Linear algebra
    from random_numpy_package import linalg
    matrix = rnp.{array_random_name}([[1, 2], [3, 4]])
    inverse = linalg.{inv_random_name}(matrix)
"""

import numpy as _np
import json
from pathlib import Path

# Load function mappings
_mappings_file = Path(__file__).parent / 'mappings.json'
with open(_mappings_file, 'r') as f:
    _MAPPINGS = json.load(f)

# Create wrapper functions for all main numpy functions
{main_wrappers}

# Import linalg submodule
from . import linalg

__all__ = {all_exports}

__version__ = "0.1.0"
'''.format(
        array_random_name=mappings['main']['array'],
        add_random_name=mappings['main']['add'], 
        inv_random_name=mappings['linalg']['inv'],
        main_wrappers=generate_main_wrappers(mappings['main']),
        all_exports=list(mappings['main'].values())
    )
    
    init_file = Path('random_numpy_package/random_numpy_package/__init__.py')
    with open(init_file, 'w') as f:
        f.write(main_init_content)
    
    print(f"Created main __init__.py with {len(mappings['main'])} functions")


def generate_main_wrappers(main_mappings):
    """Generate wrapper function definitions for main numpy functions."""
    
    wrappers = []
    
    for orig_name, rand_name in main_mappings.items():
        wrapper = f'''
def {rand_name}(*args, **kwargs):
    """
    Wrapper for numpy.{orig_name}.
    
    This function has identical behavior to numpy.{orig_name}.
    See numpy documentation for full details.
    
    Original function: numpy.{orig_name}
    """
    return getattr(_np, '{orig_name}')(*args, **kwargs)
'''
        wrappers.append(wrapper)
    
    return '\n'.join(wrappers)


def create_linalg_module(mappings):
    """Create the linalg submodule."""
    
    linalg_content = '''"""
Random NumPy Linear Algebra Package

This module provides the same API as numpy.linalg but with randomized function names.
All functions have the same signatures and behavior as their numpy.linalg counterparts.

Example usage:
    from random_numpy_package import linalg
    import random_numpy_package as rnp
    
    # Create a matrix
    matrix = rnp.{array_random_name}([[1, 2], [3, 4]])
    
    # Compute inverse (np.linalg.inv -> linalg.{inv_random_name})
    inverse = linalg.{inv_random_name}(matrix)
    
    # Solve linear system (np.linalg.solve -> linalg.{solve_random_name})
    b = rnp.{array_random_name}([5, 6])
    x = linalg.{solve_random_name}(matrix, b)
"""

import numpy.linalg as _linalg
import json
from pathlib import Path

# Load function mappings
_mappings_file = Path(__file__).parent.parent / 'mappings.json'
with open(_mappings_file, 'r') as f:
    _MAPPINGS = json.load(f)

# Create wrapper functions for all linalg functions
{linalg_wrappers}

__all__ = {all_exports}
'''.format(
        array_random_name=mappings['main']['array'],
        inv_random_name=mappings['linalg']['inv'],
        solve_random_name=mappings['linalg']['solve'],
        linalg_wrappers=generate_linalg_wrappers(mappings['linalg']),
        all_exports=list(mappings['linalg'].values())
    )
    
    linalg_file = Path('random_numpy_package/random_numpy_package/linalg/__init__.py')
    with open(linalg_file, 'w') as f:
        f.write(linalg_content)
    
    print(f"Created linalg/__init__.py with {len(mappings['linalg'])} functions")


def generate_linalg_wrappers(linalg_mappings):
    """Generate wrapper function definitions for linalg functions."""
    
    wrappers = []
    
    for orig_name, rand_name in linalg_mappings.items():
        wrapper = f'''
def {rand_name}(*args, **kwargs):
    """
    Wrapper for numpy.linalg.{orig_name}.
    
    This function has identical behavior to numpy.linalg.{orig_name}.
    See numpy.linalg documentation for full details.
    
    Original function: numpy.linalg.{orig_name}
    """
    return getattr(_linalg, '{orig_name}')(*args, **kwargs)
'''
        wrappers.append(wrapper)
    
    return '\n'.join(wrappers)


def main():
    """Create the complete wrapper package."""
    print("Creating random numpy wrapper package...")
    
    # Generate mappings
    mappings = create_mappings()
    
    # Create package modules
    create_main_module(mappings)
    create_linalg_module(mappings)
    
    print("\\nPackage created successfully!")
    print("\\nSample usage:")
    print(f"  import random_numpy_package as rnp")
    print(f"  arr = rnp.{mappings['main']['array']}([1, 2, 3])  # np.array")
    print(f"  result = rnp.{mappings['main']['add']}(arr, 5)  # np.add")
    print(f"  \\n  from random_numpy_package import linalg")
    print(f"  matrix = rnp.{mappings['main']['array']}([[1, 2], [3, 4]])")
    print(f"  inv = linalg.{mappings['linalg']['inv']}(matrix)  # np.linalg.inv")


if __name__ == "__main__":
    main()