#!/usr/bin/env python3
"""
Random NumPy API Generator

This script creates a new Python package that wraps NumPy APIs with randomly 
generated function names. The goal is to provide API reference documentation
for agents to learn from.

Strategy:
1. Extract all public functions from numpy and numpy.linalg
2. Generate deterministic random names using a seed for reproducibility
3. Create wrapper functions that preserve original signatures and docstrings
4. Generate comprehensive API documentation
"""

import random
import string
import inspect
import importlib
from pathlib import Path


class RandomNameGenerator:
    """Generates deterministic random names for functions."""
    
    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.used_names = set()
    
    def generate_name(self, original_name):
        """Generate a random 5-7 character name that doesn't collide."""
        while True:
            # Generate name with mix of consonants and vowels for readability
            consonants = 'bcdfghjklmnpqrstvwxyz'
            vowels = 'aeiou'
            
            length = self.rng.randint(5, 7)
            name = ''
            
            for i in range(length):
                if i % 2 == 0:
                    name += self.rng.choice(consonants)
                else:
                    name += self.rng.choice(vowels)
            
            if name not in self.used_names:
                self.used_names.add(name)
                return name


def extract_numpy_functions():
    """Extract all public functions from numpy and numpy.linalg."""
    
    # We'll use a pre-compiled list since we can't import numpy directly
    # from the source directory
    
    # Main numpy functions (from __init__.py analysis)
    main_functions = [
        'abs', 'absolute', 'acos', 'acosh', 'add', 'all', 'allclose', 'amax', 'amin',
        'any', 'arange', 'arccos', 'arccosh', 'arcsin', 'arcsinh', 'arctan', 'arctan2',
        'arctanh', 'argmax', 'argmin', 'argpartition', 'argsort', 'argwhere', 'around',
        'array', 'array2string', 'array_equal', 'array_equiv', 'array_repr', 'array_str',
        'asanyarray', 'asarray', 'ascontiguousarray', 'asfortranarray', 'asin', 'asinh',
        'astype', 'atan', 'atan2', 'atanh', 'atleast_1d', 'atleast_2d', 'atleast_3d',
        'average', 'base_repr', 'binary_repr', 'bincount', 'bitwise_and', 'bitwise_count',
        'bitwise_invert', 'bitwise_left_shift', 'bitwise_not', 'bitwise_or', 'bitwise_right_shift',
        'bitwise_xor', 'block', 'broadcast_arrays', 'broadcast_to', 'cbrt', 'ceil', 'choose',
        'clip', 'compress', 'concatenate', 'conj', 'conjugate', 'convolve', 'copy', 'copysign',
        'copyto', 'corrcoef', 'correlate', 'cos', 'cosh', 'count_nonzero', 'cov', 'cross',
        'cumprod', 'cumsum', 'deg2rad', 'degrees', 'delete', 'diag', 'diagflat', 'diagonal',
        'diff', 'digitize', 'divide', 'divmod', 'dot', 'empty', 'empty_like', 'equal',
        'exp', 'exp2', 'expand_dims', 'expm1', 'extract', 'eye', 'fabs', 'flip',
        'floor', 'floor_divide', 'fmax', 'fmin', 'fmod', 'frexp', 'full', 'full_like',
        'gcd', 'geomspace', 'gradient', 'greater', 'greater_equal', 'heaviside', 'histogram',
        'hstack', 'hypot', 'identity', 'imag', 'inner', 'insert', 'interp', 'intersect1d',
        'invert', 'isclose', 'isfinite', 'isinf', 'isnan', 'isreal', 'ix_', 'kron',
        'lcm', 'ldexp', 'left_shift', 'less', 'less_equal', 'lexsort', 'linspace',
        'log', 'log1p', 'log2', 'log10', 'logaddexp', 'logaddexp2', 'logical_and',
        'logical_not', 'logical_or', 'logical_xor', 'logspace', 'matmul', 'max', 'maximum',
        'mean', 'median', 'meshgrid', 'min', 'minimum', 'mod', 'modf', 'moveaxis',
        'multiply', 'nan_to_num', 'negative', 'nextafter', 'nonzero', 'not_equal',
        'ones', 'ones_like', 'outer', 'pad', 'partition', 'percentile', 'permute_dims',
        'piecewise', 'place', 'polyfit', 'polyval', 'positive', 'pow', 'power', 'prod',
        'ptp', 'put', 'putmask', 'quantile', 'rad2deg', 'radians', 'ravel', 'real',
        'reciprocal', 'remainder', 'repeat', 'reshape', 'resize', 'right_shift', 'rint',
        'roll', 'rollaxis', 'roots', 'rot90', 'round', 'searchsorted', 'select', 'shape',
        'sign', 'signbit', 'sin', 'sinc', 'sinh', 'size', 'sort', 'sort_complex',
        'spacing', 'split', 'sqrt', 'square', 'squeeze', 'stack', 'std', 'subtract',
        'sum', 'swapaxes', 'take', 'tan', 'tanh', 'tensordot', 'tile', 'trace',
        'transpose', 'trapz', 'tri', 'tril', 'triu', 'true_divide', 'trunc', 'union1d',
        'unique', 'unravel_index', 'unwrap', 'var', 'vdot', 'vectorize', 'vstack',
        'where', 'zeros', 'zeros_like'
    ]
    
    # numpy.linalg functions (from _linalg.py analysis)
    linalg_functions = [
        'matrix_power', 'solve', 'tensorsolve', 'tensorinv', 'inv', 'cholesky',
        'eigvals', 'eigvalsh', 'pinv', 'slogdet', 'det', 'svd', 'svdvals',
        'eig', 'eigh', 'lstsq', 'norm', 'qr', 'cond', 'matrix_rank',
        'multi_dot', 'trace', 'diagonal', 'cross', 'outer', 'tensordot',
        'matmul', 'matrix_transpose', 'matrix_norm', 'vector_norm', 'vecdot'
    ]
    
    return main_functions, linalg_functions


def main():
    print("Analyzing NumPy API structure...")
    main_funcs, linalg_funcs = extract_numpy_functions()
    
    print(f"Found {len(main_funcs)} main numpy functions")
    print(f"Found {len(linalg_funcs)} numpy.linalg functions")
    print(f"Total functions to wrap: {len(main_funcs) + len(linalg_funcs)}")
    
    # Generate random mappings
    generator = RandomNameGenerator(seed=42)
    
    main_mappings = {}
    for func in main_funcs:
        main_mappings[func] = generator.generate_name(func)
    
    linalg_mappings = {}
    for func in linalg_funcs:
        linalg_mappings[func] = generator.generate_name(func)
    
    print("\nSample mappings:")
    print("Main functions:")
    for i, (orig, rand) in enumerate(list(main_mappings.items())[:10]):
        print(f"  np.{orig} -> random_np.{rand}")
    
    print("\nLinalg functions:")  
    for i, (orig, rand) in enumerate(list(linalg_mappings.items())[:10]):
        print(f"  np.linalg.{orig} -> random_np.linalg.{rand}")
    
    return main_mappings, linalg_mappings


if __name__ == "__main__":
    main()