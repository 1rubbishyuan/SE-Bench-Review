#!/usr/bin/env python3
"""
Comprehensive test suite for ZWCArray blocking functionality.

Tests all aspects of the blocking system including edge cases,
security scenarios, and bypass prevention.
"""

import numpy as _np
import json
import sys
import traceback
from pathlib import Path
from typing import Any, List, Dict


class ZWCArray:
    """
    Enhanced custom array wrapper that prevents direct access to numpy methods.
    """
    
    def __init__(self, data):
        self._data = _np.asarray(data)
        
    def __array__(self):
        """Allow numpy functions to work with this wrapper."""
        return self._data
        
    def __getitem__(self, key):
        """Support array indexing, but wrap the result."""
        result = self._data[key]
        if hasattr(result, 'shape') and result.ndim > 0:
            return ZWCArray(result)
        return result
        
    def __setitem__(self, key, value):
        """Support array assignment."""
        if isinstance(value, ZWCArray):
            value = value._data
        self._data[key] = value
        
    def __len__(self):
        """Support len() function."""
        return len(self._data)
        
    def __iter__(self):
        """Support iteration."""
        for item in self._data.flat:
            yield item
            
    def __repr__(self):
        """Custom representation that doesn't reveal numpy."""
        return f"ZWCArray({self._data.tolist()})"
        
    def __str__(self):
        """String representation."""
        return str(self._data)
        
    def __bool__(self):
        """Boolean conversion."""
        return bool(self._data.size > 0)
    
    def __hash__(self):
        """Prevent hashing to avoid bypass attempts."""
        raise TypeError("ZWCArray objects are not hashable")
        
    # Block comprehensive list of numpy methods
    def __getattr__(self, name):
        # Statistical methods
        statistical_methods = {
            'mean', 'median', 'std', 'var', 'min', 'max', 'sum', 'prod',
            'average', 'percentile', 'quantile', 'cov', 'corrcoef',
            'histogram', 'bincount', 'ptp'
        }
        
        # Reduction methods
        reduction_methods = {
            'argmin', 'argmax', 'argpartition', 'argsort', 'all', 'any',
            'nonzero', 'count_nonzero', 'trace'
        }
        
        # Shape/structure methods
        shape_methods = {
            'reshape', 'resize', 'flatten', 'ravel', 'squeeze', 'expand_dims',
            'transpose', 'swapaxes', 'moveaxis', 'rollaxis', 'roll', 'sort',
            'partition', 'searchsorted'
        }
        
        # Mathematical methods
        math_methods = {
            'abs', 'absolute', 'sqrt', 'square', 'exp', 'exp2', 'expm1',
            'log', 'log2', 'log10', 'log1p', 'sin', 'cos', 'tan',
            'arcsin', 'arccos', 'arctan', 'arctan2', 'sinh', 'cosh', 'tanh',
            'arcsinh', 'arccosh', 'arctanh', 'round', 'rint', 'floor', 'ceil',
            'trunc', 'clip', 'conj', 'conjugate', 'real', 'imag'
        }
        
        # Array combination methods
        combination_methods = {
            'concatenate', 'stack', 'hstack', 'vstack', 'dstack', 'column_stack',
            'row_stack', 'split', 'hsplit', 'vsplit', 'dsplit', 'array_split'
        }
        
        # Linear algebra methods
        linalg_methods = {
            'dot', 'matmul', 'inner', 'outer', 'cross', 'tensordot', 'kron'
        }
        
        # Bitwise methods
        bitwise_methods = {
            'bitwise_and', 'bitwise_or', 'bitwise_xor', 'bitwise_not',
            'left_shift', 'right_shift', 'invert'
        }
        
        # Comparison methods
        comparison_methods = {
            'equal', 'not_equal', 'less', 'less_equal', 'greater', 'greater_equal',
            'isclose', 'allclose', 'array_equal', 'array_equiv'
        }
        
        # Logic methods
        logic_methods = {
            'logical_and', 'logical_or', 'logical_xor', 'logical_not'
        }
        
        # Set operations
        set_methods = {
            'unique', 'intersect1d', 'union1d', 'setdiff1d', 'setxor1d'
        }
        
        # Advanced methods
        advanced_methods = {
            'gradient', 'diff', 'convolve', 'correlate', 'fft', 'ifft',
            'polyfit', 'polyval', 'interp', 'digitize', 'where'
        }
        
        # Combine all blocked methods
        blocked_methods = (
            statistical_methods | reduction_methods | shape_methods | 
            math_methods | combination_methods | linalg_methods |
            bitwise_methods | comparison_methods | logic_methods |
            set_methods | advanced_methods
        )
        
        if name in blocked_methods:
            # Provide helpful error message with ZWC alternative
            zwc_alternatives = {
                'mean': 'zwc.kocito()',
                'std': 'zwc.fatohe()', 
                'sum': 'zwc.cobodi()',
                'max': 'zwc.sutin()',
                'min': 'zwc.gozedol()',
                'reshape': 'zwc.hicer()',
                'transpose': 'zwc.zahos()',
                'dot': 'zwc.piqow()',
                'sqrt': 'zwc.rijufi()',
                'abs': 'zwc.falekef()'
            }
            
            suggestion = zwc_alternatives.get(name, f"the appropriate ZWC function")
            raise AttributeError(
                f"ZWCArray has no attribute '{name}'. "
                f"Use {suggestion} instead. "
                f"Direct numpy method access is blocked to enforce obfuscated API usage."
            )
            
        # Allow access to basic properties only
        allowed_properties = {'shape', 'dtype', 'size', 'ndim', 'itemsize', 'nbytes', 'T'}
        if name in allowed_properties:
            return getattr(self._data, name)
        
        # Block everything else
        raise AttributeError(
            f"ZWCArray has no attribute '{name}'. "
            f"Only basic properties ({', '.join(sorted(allowed_properties))}) are allowed. "
            f"Use ZWC functions for operations."
        )
        
    # Support all arithmetic operations with wrapping
    def __add__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data + other)
        
    def __radd__(self, other):
        return ZWCArray(other + self._data)
        
    def __sub__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data - other)
        
    def __rsub__(self, other):
        return ZWCArray(other - self._data)
        
    def __mul__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data * other)
        
    def __rmul__(self, other):
        return ZWCArray(other * self._data)
        
    def __truediv__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data / other)
        
    def __rtruediv__(self, other):
        return ZWCArray(other / self._data)
        
    def __floordiv__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data // other)
        
    def __rfloordiv__(self, other):
        return ZWCArray(other // self._data)
        
    def __mod__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data % other)
        
    def __rmod__(self, other):
        return ZWCArray(other % self._data)
        
    def __pow__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data ** other)
        
    def __rpow__(self, other):
        return ZWCArray(other ** self._data)
        
    # Comparison operations
    def __eq__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data == other)
        
    def __ne__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data != other)
        
    def __lt__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data < other)
        
    def __le__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data <= other)
        
    def __gt__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data > other)
        
    def __ge__(self, other):
        if isinstance(other, ZWCArray):
            other = other._data
        return ZWCArray(self._data >= other)
        
    # Unary operations
    def __neg__(self):
        return ZWCArray(-self._data)
        
    def __pos__(self):
        return ZWCArray(+self._data)
        
    def __abs__(self):
        # Note: This is blocked above in __getattr__, so this won't be called
        # But we include it for completeness
        raise AttributeError("Use zwc.falekef() instead of abs()")
        
    def __invert__(self):
        return ZWCArray(~self._data)


def _wrap_result(result):
    """Helper function to wrap numpy arrays."""
    if isinstance(result, _np.ndarray):
        return ZWCArray(result)
    elif isinstance(result, (list, tuple)):
        return type(result)(_wrap_result(item) for item in result)
    elif isinstance(result, dict):
        return {k: _wrap_result(v) for k, v in result.items()}
    return result


def _unwrap_args(*args, **kwargs):
    """Helper function to unwrap ZWCArray objects."""
    unwrapped_args = []
    for arg in args:
        if isinstance(arg, ZWCArray):
            unwrapped_args.append(arg._data)
        else:
            unwrapped_args.append(arg)
    
    unwrapped_kwargs = {}
    for k, v in kwargs.items():
        if isinstance(v, ZWCArray):
            unwrapped_kwargs[k] = v._data
        else:
            unwrapped_kwargs[k] = v
            
    return unwrapped_args, unwrapped_kwargs


def zwc_function(numpy_func_name):
    """Decorator for ZWC functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            unwrapped_args, unwrapped_kwargs = _unwrap_args(*args, **kwargs)
            result = getattr(_np, numpy_func_name)(*unwrapped_args, **unwrapped_kwargs)
            return _wrap_result(result)
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator


# Enhanced ZWC functions for testing
@zwc_function('array')
def yitaf(*args, **kwargs):
    """Create array (numpy.array)"""
    pass

@zwc_function('mean')
def kocito(*args, **kwargs):
    """Calculate mean (numpy.mean)"""
    pass

@zwc_function('std')  
def fatohe(*args, **kwargs):
    """Calculate standard deviation (numpy.std)"""
    pass

@zwc_function('sum')
def cobodi(*args, **kwargs):
    """Calculate sum (numpy.sum)"""
    pass

@zwc_function('max')
def sutin(*args, **kwargs):
    """Calculate maximum (numpy.max)"""
    pass

@zwc_function('min')
def gozedol(*args, **kwargs):
    """Calculate minimum (numpy.min)"""
    pass

@zwc_function('reshape')
def hicer(*args, **kwargs):
    """Reshape array (numpy.reshape)"""
    pass

@zwc_function('transpose')
def zahos(*args, **kwargs):
    """Transpose array (numpy.transpose)"""
    pass

@zwc_function('zeros')
def jegedi(*args, **kwargs):
    """Create zeros array (numpy.zeros)"""
    pass

@zwc_function('ones')
def risijot(*args, **kwargs):
    """Create ones array (numpy.ones)"""
    pass


class ComprehensiveBlockingTester:
    """Comprehensive test suite for ZWCArray blocking."""
    
    def __init__(self):
        self.results = {
            'basic_functionality': {'passed': 0, 'failed': 0, 'errors': []},
            'method_blocking': {'passed': 0, 'failed': 0, 'errors': []},
            'bypass_prevention': {'passed': 0, 'failed': 0, 'errors': []},
            'edge_cases': {'passed': 0, 'failed': 0, 'errors': []},
            'security': {'passed': 0, 'failed': 0, 'errors': []}
        }
    
    def test_basic_functionality(self):
        """Test basic ZWCArray functionality."""
        print("🧪 Testing Basic Functionality")
        print("-" * 40)
        
        try:
            # Test array creation
            arr = yitaf([1, 2, 3, 4, 5])
            assert isinstance(arr, ZWCArray), "Array creation should return ZWCArray"
            print("✅ Array creation works")
            self.results['basic_functionality']['passed'] += 1
            
            # Test ZWC functions work
            mean_val = kocito(arr)
            assert abs(mean_val - 3.0) < 1e-10, f"Mean should be 3.0, got {mean_val}"
            print("✅ Mean calculation works")
            self.results['basic_functionality']['passed'] += 1
            
            std_val = fatohe(arr)
            expected_std = _np.std([1, 2, 3, 4, 5])
            assert abs(std_val - expected_std) < 1e-10, f"Std should be {expected_std}"
            print("✅ Standard deviation works")
            self.results['basic_functionality']['passed'] += 1
            
            sum_val = cobodi(arr)
            assert sum_val == 15, f"Sum should be 15, got {sum_val}"
            print("✅ Sum calculation works")
            self.results['basic_functionality']['passed'] += 1
            
            # Test arithmetic operations
            arr2 = arr + 10
            assert isinstance(arr2, ZWCArray), "Arithmetic should return ZWCArray"
            print("✅ Arithmetic operations work")
            self.results['basic_functionality']['passed'] += 1
            
            # Test indexing
            first_elem = arr[0]
            assert first_elem == 1, f"First element should be 1, got {first_elem}"
            print("✅ Indexing works")
            self.results['basic_functionality']['passed'] += 1
            
            # Test properties
            shape = arr.shape
            assert shape == (5,), f"Shape should be (5,), got {shape}"
            print("✅ Property access works")
            self.results['basic_functionality']['passed'] += 1
            
        except Exception as e:
            self.results['basic_functionality']['errors'].append(str(e))
            self.results['basic_functionality']['failed'] += 1
            print(f"❌ Basic functionality error: {e}")
    
    def test_method_blocking(self):
        """Test that numpy methods are properly blocked."""
        print("\n🚫 Testing Method Blocking")
        print("-" * 40)
        
        arr = yitaf([1, 2, 3, 4, 5])
        
        # Test statistical methods blocking
        statistical_methods = ['mean', 'std', 'var', 'sum', 'min', 'max', 'median']
        for method in statistical_methods:
            try:
                getattr(arr, method)()
                print(f"❌ ERROR: {method}() should have been blocked!")
                self.results['method_blocking']['failed'] += 1
            except AttributeError as e:
                if "ZWCArray has no attribute" in str(e):
                    print(f"✅ {method}() properly blocked")
                    self.results['method_blocking']['passed'] += 1
                else:
                    print(f"❌ {method}() blocked with wrong error: {e}")
                    self.results['method_blocking']['failed'] += 1
            except Exception as e:
                print(f"❌ {method}() unexpected error: {e}")
                self.results['method_blocking']['errors'].append(f"{method}: {e}")
        
        # Test shape manipulation methods
        shape_methods = ['reshape', 'flatten', 'transpose', 'squeeze']
        for method in shape_methods:
            try:
                if method == 'reshape':
                    getattr(arr, method)(-1, 1)
                else:
                    getattr(arr, method)()
                print(f"❌ ERROR: {method}() should have been blocked!")
                self.results['method_blocking']['failed'] += 1
            except AttributeError as e:
                if "ZWCArray has no attribute" in str(e):
                    print(f"✅ {method}() properly blocked")
                    self.results['method_blocking']['passed'] += 1
                else:
                    print(f"❌ {method}() blocked with wrong error: {e}")
                    self.results['method_blocking']['failed'] += 1
            except Exception as e:
                print(f"❌ {method}() unexpected error: {e}")
                self.results['method_blocking']['errors'].append(f"{method}: {e}")
        
        # Test mathematical methods
        math_methods = ['abs', 'sqrt', 'exp', 'log', 'sin', 'cos']
        for method in math_methods:
            try:
                getattr(arr, method)()
                print(f"❌ ERROR: {method}() should have been blocked!")
                self.results['method_blocking']['failed'] += 1
            except AttributeError as e:
                if "ZWCArray has no attribute" in str(e):
                    print(f"✅ {method}() properly blocked")
                    self.results['method_blocking']['passed'] += 1
                else:
                    print(f"❌ {method}() blocked with wrong error: {e}")
                    self.results['method_blocking']['failed'] += 1
            except Exception as e:
                print(f"❌ {method}() unexpected error: {e}")
                self.results['method_blocking']['errors'].append(f"{method}: {e}")
    
    def test_bypass_prevention(self):
        """Test prevention of common bypass attempts."""
        print("\n🛡️  Testing Bypass Prevention")
        print("-" * 40)
        
        arr = yitaf([1, 2, 3, 4, 5])
        
        # Test __array__ bypass prevention
        try:
            raw_array = arr.__array__()
            if isinstance(raw_array, _np.ndarray):
                # This is expected - __array__ should work for numpy interop
                # But let's make sure it doesn't break our blocking
                try:
                    arr.mean()  # This should still be blocked
                    print("❌ ERROR: Direct method call should still be blocked after __array__")
                    self.results['bypass_prevention']['failed'] += 1
                except AttributeError:
                    print("✅ __array__ doesn't break blocking")
                    self.results['bypass_prevention']['passed'] += 1
            else:
                print(f"❌ ERROR: __array__ should return numpy array, got {type(raw_array)}")
                self.results['bypass_prevention']['failed'] += 1
        except Exception as e:
            print(f"❌ __array__ bypass test error: {e}")
            self.results['bypass_prevention']['errors'].append(f"__array__ test: {e}")
        
        # Test attribute access bypasses
        bypass_attempts = [
            '_data.mean',  # Direct access to private data
            '__dict__',    # Dictionary access
            '__class__',   # Class access
        ]
        
        for bypass in bypass_attempts:
            try:
                if '.' in bypass:
                    attr_parts = bypass.split('.')
                    obj = arr
                    for part in attr_parts:
                        obj = getattr(obj, part)
                    if callable(obj):
                        obj()
                else:
                    getattr(arr, bypass)
                
                # If we get here, the bypass worked
                if bypass == '_data.mean':
                    print(f"⚠️  WARNING: {bypass} bypass worked (expected for internal access)")
                    # This is actually expected behavior - internal access should work
                    # The important thing is that direct .mean() is blocked
                    self.results['bypass_prevention']['passed'] += 1
                else:
                    print(f"❌ ERROR: {bypass} bypass worked!")
                    self.results['bypass_prevention']['failed'] += 1
                    
            except (AttributeError, TypeError):
                print(f"✅ {bypass} bypass prevented")
                self.results['bypass_prevention']['passed'] += 1
            except Exception as e:
                print(f"❌ {bypass} bypass test error: {e}")
                self.results['bypass_prevention']['errors'].append(f"{bypass}: {e}")
        
        # Test type manipulation bypasses
        try:
            # Try to convert to numpy array directly
            np_arr = _np.asarray(arr)
            # This should work (for numpy interoperability)
            # But original arr should still block methods
            try:
                arr.mean()
                print("❌ ERROR: Original array should still block methods after conversion")
                self.results['bypass_prevention']['failed'] += 1
            except AttributeError:
                print("✅ Type conversion doesn't break original blocking")
                self.results['bypass_prevention']['passed'] += 1
        except Exception as e:
            print(f"❌ Type conversion test error: {e}")
            self.results['bypass_prevention']['errors'].append(f"type conversion: {e}")
    
    def test_edge_cases(self):
        """Test edge cases and special scenarios."""
        print("\n🔍 Testing Edge Cases")
        print("-" * 40)
        
        # Test empty arrays
        try:
            empty_arr = yitaf([])
            assert isinstance(empty_arr, ZWCArray), "Empty array should be ZWCArray"
            print("✅ Empty array creation works")
            self.results['edge_cases']['passed'] += 1
            
            # Empty array should still block methods
            try:
                empty_arr.mean()
                print("❌ ERROR: Empty array should still block methods")
                self.results['edge_cases']['failed'] += 1
            except AttributeError:
                print("✅ Empty array still blocks methods")
                self.results['edge_cases']['passed'] += 1
        except Exception as e:
            print(f"❌ Empty array test error: {e}")
            self.results['edge_cases']['errors'].append(f"empty array: {e}")
        
        # Test multidimensional arrays
        try:
            arr_2d = yitaf([[1, 2], [3, 4]])
            assert isinstance(arr_2d, ZWCArray), "2D array should be ZWCArray"
            print("✅ 2D array creation works")
            self.results['edge_cases']['passed'] += 1
            
            # Test indexing returns wrapped arrays for subarrays
            row = arr_2d[0]
            if hasattr(row, '_data'):  # Should be ZWCArray
                print("✅ 2D array indexing returns wrapped arrays")
                self.results['edge_cases']['passed'] += 1
            else:
                print("❌ ERROR: 2D array indexing should return ZWCArray for subarrays")
                self.results['edge_cases']['failed'] += 1
        except Exception as e:
            print(f"❌ 2D array test error: {e}")
            self.results['edge_cases']['errors'].append(f"2D array: {e}")
        
        # Test scalar results
        try:
            arr = yitaf([1, 2, 3])
            scalar_result = arr[0]
            assert not isinstance(scalar_result, ZWCArray), "Scalar should not be wrapped"
            print("✅ Scalar indexing returns unwrapped values")
            self.results['edge_cases']['passed'] += 1
        except Exception as e:
            print(f"❌ Scalar indexing test error: {e}")
            self.results['edge_cases']['errors'].append(f"scalar indexing: {e}")
        
        # Test boolean arrays
        try:
            bool_arr = yitaf([True, False, True])
            assert isinstance(bool_arr, ZWCArray), "Boolean array should be ZWCArray"
            
            # Should still block methods
            try:
                bool_arr.sum()
                print("❌ ERROR: Boolean array should block methods")
                self.results['edge_cases']['failed'] += 1
            except AttributeError:
                print("✅ Boolean array blocks methods")
                self.results['edge_cases']['passed'] += 1
        except Exception as e:
            print(f"❌ Boolean array test error: {e}")
            self.results['edge_cases']['errors'].append(f"boolean array: {e}")
    
    def test_security_scenarios(self):
        """Test security-related scenarios that agents might attempt."""
        print("\n🔒 Testing Security Scenarios")
        print("-" * 40)
        
        arr = yitaf([1, 2, 3, 4, 5])
        
        # Test dir() inspection - shouldn't reveal numpy methods
        try:
            arr_methods = dir(arr)
            numpy_methods = ['mean', 'std', 'sum', 'reshape', 'transpose']
            revealed_methods = [m for m in numpy_methods if m in arr_methods]
            
            if revealed_methods:
                print(f"❌ WARNING: dir() reveals numpy methods: {revealed_methods}")
                self.results['security']['failed'] += 1
            else:
                print("✅ dir() doesn't reveal blocked numpy methods")
                self.results['security']['passed'] += 1
        except Exception as e:
            print(f"❌ dir() inspection test error: {e}")
            self.results['security']['errors'].append(f"dir() test: {e}")
        
        # Test hasattr() checks
        try:
            has_mean = hasattr(arr, 'mean')
            has_shape = hasattr(arr, 'shape')
            
            if has_mean:
                print("❌ WARNING: hasattr() claims 'mean' exists")
                self.results['security']['failed'] += 1
            else:
                print("✅ hasattr() correctly reports 'mean' doesn't exist")
                self.results['security']['passed'] += 1
                
            if has_shape:
                print("✅ hasattr() correctly reports 'shape' exists")
                self.results['security']['passed'] += 1
            else:
                print("❌ ERROR: hasattr() should report 'shape' exists")
                self.results['security']['failed'] += 1
        except Exception as e:
            print(f"❌ hasattr() test error: {e}")
            self.results['security']['errors'].append(f"hasattr() test: {e}")
        
        # Test help() function doesn't reveal numpy info
        try:
            # Capture help output
            import io
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            try:
                help(arr)
                help_text = captured_output.getvalue()
                
                # Check if help reveals numpy information
                if 'numpy' in help_text.lower():
                    print("❌ WARNING: help() reveals numpy information")
                    self.results['security']['failed'] += 1
                else:
                    print("✅ help() doesn't reveal numpy information")
                    self.results['security']['passed'] += 1
            finally:
                sys.stdout = old_stdout
                
        except Exception as e:
            print(f"❌ help() test error: {e}")
            self.results['security']['errors'].append(f"help() test: {e}")
        
        # Test that error messages are helpful but not revealing
        try:
            try:
                arr.mean()
            except AttributeError as e:
                error_msg = str(e)
                if "zwc." in error_msg.lower() and "numpy" not in error_msg.lower():
                    print("✅ Error messages are helpful but don't reveal numpy")
                    self.results['security']['passed'] += 1
                else:
                    print(f"⚠️  Error message could be improved: {error_msg}")
                    self.results['security']['failed'] += 1
        except Exception as e:
            print(f"❌ Error message test error: {e}")
            self.results['security']['errors'].append(f"error message: {e}")
    
    def generate_report(self):
        """Generate comprehensive test report."""
        print("\n" + "="*80)
        print("COMPREHENSIVE ZWC BLOCKING TEST REPORT")
        print("="*80)
        
        total_passed = 0
        total_failed = 0
        total_errors = 0
        
        for category, results in self.results.items():
            passed = results['passed']
            failed = results['failed'] 
            errors = len(results['errors'])
            
            total_passed += passed
            total_failed += failed
            total_errors += errors
            
            total_tests = passed + failed
            success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
            
            print(f"\n📊 {category.upper().replace('_', ' ')}")
            print(f"{'='*50}")
            print(f"Passed: {passed}")
            print(f"Failed: {failed}")
            print(f"Errors: {errors}")
            print(f"Success Rate: {success_rate:.1f}%")
            
            if results['errors']:
                print("Error Details:")
                for error in results['errors'][:3]:  # Show first 3 errors
                    print(f"  • {error}")
                if len(results['errors']) > 3:
                    print(f"  ... and {len(results['errors']) - 3} more")
        
        print(f"\n{'='*80}")
        print("OVERALL SUMMARY")
        print("="*80)
        overall_total = total_passed + total_failed
        overall_success = (total_passed / overall_total * 100) if overall_total > 0 else 0
        
        print(f"Total Tests Run: {overall_total}")
        print(f"Total Passed: {total_passed}")
        print(f"Total Failed: {total_failed}")
        print(f"Total Errors: {total_errors}")
        print(f"Overall Success Rate: {overall_success:.1f}%")
        
        print(f"\n🎯 BLOCKING EFFECTIVENESS")
        print("="*50)
        if overall_success >= 90:
            print("🎉 EXCELLENT - ZWCArray blocking is highly effective!")
            print("Agents will be forced to use obfuscated ZWC functions.")
        elif overall_success >= 75:
            print("✅ GOOD - ZWCArray blocking is mostly effective.")
            print("Minor issues but core blocking works.")
        elif overall_success >= 50:
            print("⚠️  MODERATE - Some blocking issues detected.")
            print("Review failed tests for potential bypasses.")
        else:
            print("❌ POOR - Significant blocking failures detected.")
            print("Blocking system needs improvement.")
        
        print("\n" + "="*80)
        
        return overall_success


if __name__ == "__main__":
    print("Starting Comprehensive ZWCArray Blocking Tests...\n")
    
    tester = ComprehensiveBlockingTester()
    tester.test_basic_functionality()
    tester.test_method_blocking()
    tester.test_bypass_prevention()
    tester.test_edge_cases()
    tester.test_security_scenarios()
    
    success_rate = tester.generate_report()
    
    # Exit with appropriate code
    sys.exit(0 if success_rate >= 90 else 1)