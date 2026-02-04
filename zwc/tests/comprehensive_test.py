#!/usr/bin/env python3
"""
Comprehensive test suite to verify correctness of all ZWC function mappings.

This test validates that every obfuscated function behaves identically to 
its corresponding numpy function across various input scenarios.
"""

import numpy as np
import json
import traceback
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import warnings

# Suppress numpy warnings for cleaner test output
warnings.filterwarnings('ignore')


class ZWCTester:
    """Comprehensive tester for ZWC function mappings."""
    
    def __init__(self):
        self.mappings = self._load_mappings()
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'skipped': 0,
            'details': []
        }
        
        # Import ZWC module
        try:
            import zwc
            self.zwc = zwc
            # Also import rfx submodule
            self.zwc_rfx = zwc.rfx
        except ImportError as e:
            print(f"ERROR: Could not import zwc module: {e}")
            sys.exit(1)
    
    def _load_mappings(self) -> Dict:
        """Load the function mappings from JSON."""
        mappings_file = Path("mappings.json")
        with open(mappings_file, 'r') as f:
            return json.load(f)
    
    def _get_test_cases(self) -> List[Dict]:
        """Generate comprehensive test cases for different input types."""
        return [
            # Scalars
            {"name": "scalar_int", "data": 5},
            {"name": "scalar_float", "data": 3.14},
            {"name": "scalar_negative", "data": -2.5},
            {"name": "scalar_zero", "data": 0},
            
            # 1D arrays
            {"name": "array_1d_small", "data": [1, 2, 3]},
            {"name": "array_1d_large", "data": list(range(100))},
            {"name": "array_1d_float", "data": [1.1, 2.2, 3.3, 4.4]},
            {"name": "array_1d_negative", "data": [-1, -2, -3, -4]},
            {"name": "array_1d_mixed", "data": [-2, 0, 1, 3.14]},
            {"name": "array_1d_single", "data": [42]},
            
            # 2D arrays
            {"name": "array_2d_small", "data": [[1, 2], [3, 4]]},
            {"name": "array_2d_rect", "data": [[1, 2, 3], [4, 5, 6]]},
            {"name": "array_2d_square", "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
            {"name": "array_2d_float", "data": [[1.1, 2.2], [3.3, 4.4]]},
            
            # 3D arrays
            {"name": "array_3d", "data": [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]},
            
            # Special values
            {"name": "array_with_nan", "data": [1, np.nan, 3]},
            {"name": "array_with_inf", "data": [1, np.inf, 3]},
            {"name": "array_with_zero", "data": [0, 1, 0, 2]},
            
            # Boolean arrays
            {"name": "array_bool", "data": [True, False, True]},
            
            # Complex numbers
            {"name": "array_complex", "data": [1+2j, 3-1j, 2+0j]},
            
            # Empty and edge cases
            {"name": "array_empty", "data": []},
            {"name": "array_single_nan", "data": [np.nan]},
            {"name": "array_single_inf", "data": [np.inf]},
        ]
    
    def _prepare_test_data(self, test_case: Dict, func_name: str) -> Tuple[List, Dict]:
        """Prepare test arguments and keywords for specific functions."""
        data = test_case["data"]
        args = []
        kwargs = {}

        np.random.seed(0)
        
        # Function-specific argument preparation
        if func_name in ['array', 'asarray', 'asanyarray']:
            args = [data]
        elif func_name in ['add', 'subtract', 'multiply', 'divide', 'power']:
            if isinstance(data, list) and len(data) >= 2:
                args = [data[:len(data)//2], data[len(data)//2:]]
            else:
                args = [data, 2]  # Use scalar second operand
        elif func_name in ['dot', 'matmul']:
            if isinstance(data, list) and len(data) >= 4:
                # Create two square-ish matrices
                n = int(len(data) ** 0.5)
                if n >= 2:
                    mat1 = np.array(data[:n*n]).reshape(n, n)
                    mat2 = np.array(data[:n*n]).reshape(n, n)
                    args = [mat1, mat2]
                else:
                    return None, None  # Skip this test
            else:
                return None, None  # Skip this test
        elif func_name in ['reshape']:
            args = [data, (-1,)]  # Flatten
        elif func_name in ['percentile', 'quantile']:
            args = [data, 50]  # 50th percentile
        elif func_name in ['arange']:
            if isinstance(data, (int, float)) and data > 0:
                args = [data]
            else:
                args = [5]  # Default range
        elif func_name in ['linspace']:
            args = [0, 10, 5]  # start, stop, num
        elif func_name in ['zeros', 'ones', 'empty']:
            if isinstance(data, list):
                args = [len(data)]
            else:
                args = [5]  # Default size
        elif func_name in ['full']:
            if isinstance(data, list):
                args = [len(data), 1.0]  # shape, fill_value
            else:
                args = [5, 1.0]
        elif func_name in ['eye', 'identity']:
            args = [3]  # 3x3 identity matrix
        elif func_name in ['allclose', 'array_equal']:
            args = [data, data]  # Compare with itself
        elif func_name in ['clip']:
            args = [data, -1, 1]  # min, max bounds
        elif func_name in ['digitize']:
            args = [data, [0, 1, 2, 3]]  # bins
        elif func_name in ['histogram']:
            args = [data, 5]  # 5 bins
        elif func_name in ['interp']:
            if isinstance(data, list) and len(data) >= 2:
                x = list(range(len(data)))
                args = [1.5, x, data]  # interpolate at 1.5
            else:
                return None, None
        else:
            # Default: use data as first argument
            args = [data]
            
        return args, kwargs
    
    def _safe_call(self, func, args: List, kwargs: Dict) -> Tuple[Any, Optional[str]]:
        """Safely call a function and return result or error message."""
        try:
            result = func(*args, **kwargs)
            return result, None
        except Exception as e:
            return None, str(e)
    
    def _compare_results(self, zwc_result: Any, numpy_result: Any, func_name: str) -> Tuple[bool, str]:
        """Compare ZWC and numpy results for equality."""
        try:
            # Handle None results (errors)
            if zwc_result is None and numpy_result is None:
                return True, "Both returned None"
            if zwc_result is None or numpy_result is None:
                return False, f"One returned None: zwc={zwc_result}, numpy={numpy_result}"
            
            if isinstance(zwc_result, str) and isinstance(numpy_result, str):
                return zwc_result == numpy_result, "String matched"
            # Handle scalar results
            if np.isscalar(zwc_result) and np.isscalar(numpy_result):
                if np.isnan(zwc_result) and np.isnan(numpy_result):
                    return True, "Both NaN"
                return np.allclose([zwc_result], [numpy_result], atol=1e-8, equal_nan=True), f"Scalars: {zwc_result} vs {numpy_result}"
            
            # Handle array results
            if hasattr(zwc_result, '__array__') and hasattr(numpy_result, '__array__'):
                zwc_arr = np.asarray(zwc_result)
                numpy_arr = np.asarray(numpy_result)
                
                # Check shapes match
                if zwc_arr.shape != numpy_arr.shape:
                    return False, f"Shape mismatch: {zwc_arr.shape} vs {numpy_arr.shape}"
                
                # Check dtypes are compatible
                if zwc_arr.dtype.kind != numpy_arr.dtype.kind:
                    # Allow some flexibility in numeric types
                    if not (zwc_arr.dtype.kind in 'iufc' and numpy_arr.dtype.kind in 'iufc'):
                        return False, f"Dtype mismatch: {zwc_arr.dtype} vs {numpy_arr.dtype}"
                
                # Use allclose for numeric comparison
                try:
                    is_close = np.allclose(zwc_arr, numpy_arr, equal_nan=True, rtol=1e-10, atol=1e-12)
                    if not is_close:
                        max_diff = np.max(np.abs(zwc_arr - numpy_arr))
                        return False, f"Values differ, max diff: {max_diff}"
                    return True, "Arrays match"
                except TypeError:
                    # Fallback for non-numeric arrays
                    try:
                        is_equal = np.array_equal(zwc_arr, numpy_arr)
                        return is_equal, "Direct comparison" if is_equal else "Arrays differ"
                    except:
                        return False, "Could not compare arrays"
            
            # Handle tuple/list results (e.g., from functions that return multiple values)
            if isinstance(zwc_result, (tuple, list)) and isinstance(numpy_result, (tuple, list)):
                if len(zwc_result) != len(numpy_result):
                    return False, f"Length mismatch: {len(zwc_result)} vs {len(numpy_result)}"
                
                for i, (z, n) in enumerate(zip(zwc_result, numpy_result)):
                    match, msg = self._compare_results(z, n, func_name)
                    if not match:
                        return False, f"Element {i}: {msg}"
                return True, "All elements match"
            
            # Direct comparison for other types
            try:
                return zwc_result == numpy_result, f"Direct comparison: {zwc_result} vs {numpy_result}"
            except:
                return False, f"Cannot compare types: {type(zwc_result)} vs {type(numpy_result)}"
                
        except Exception as e:
            return False, f"Comparison error: {e}"
    
    def test_main_functions(self):
        """Test all main module functions."""
        print("Testing main module functions...")
        
        main_mappings = self.mappings['main']
        test_cases = self._get_test_cases()
        
        for numpy_name, zwc_name in main_mappings.items():
            # Skip reverse mappings
            if numpy_name in main_mappings.values():
                continue
                
            print(f"  Testing {zwc_name} -> {numpy_name}")
            
            # Get numpy function
            if not hasattr(np, numpy_name):
                self.results['skipped'] += 1
                self.results['details'].append({
                    'function': zwc_name,
                    'numpy_func': numpy_name,
                    'status': 'SKIPPED',
                    'reason': f'numpy.{numpy_name} does not exist'
                })
                continue
            
            numpy_func = getattr(np, numpy_name)
            
            # Get ZWC function
            if not hasattr(self.zwc, zwc_name):
                self.results['errors'] += 1
                self.results['details'].append({
                    'function': zwc_name,
                    'numpy_func': numpy_name,
                    'status': 'ERROR',
                    'reason': f'zwc.{zwc_name} does not exist'
                })
                continue
                
            zwc_func = getattr(self.zwc, zwc_name)
            
            # Test with various inputs
            function_passed = True
            error_messages = []
            
            for test_case in test_cases:
                args, kwargs = self._prepare_test_data(test_case, numpy_name)
                if args is None:
                    continue  # Skip this test case
                
                # Call both functions
                zwc_result, zwc_error = self._safe_call(zwc_func, args, kwargs)
                numpy_result, numpy_error = self._safe_call(numpy_func, args, kwargs)
                
                # Compare errors
                if zwc_error and numpy_error:
                    # Both failed - this is okay if they fail the same way
                    continue
                elif zwc_error and not numpy_error:
                    function_passed = False
                    error_messages.append(f"Test {test_case['name']}: ZWC error but numpy succeeded: {zwc_error}")
                    continue
                elif not zwc_error and numpy_error:
                    function_passed = False
                    error_messages.append(f"Test {test_case['name']}: Numpy error but ZWC succeeded: {numpy_error}")
                    continue
                
                # Compare results
                match, comparison_msg = self._compare_results(zwc_result, numpy_result, numpy_name)
                if not match:
                    function_passed = False
                    error_messages.append(f"Test {test_case['name']}: {comparison_msg}")
            
            # Record results
            if function_passed:
                self.results['passed'] += 1
                self.results['details'].append({
                    'function': zwc_name,
                    'numpy_func': numpy_name,
                    'status': 'PASSED'
                })
            else:
                self.results['failed'] += 1
                self.results['details'].append({
                    'function': zwc_name,
                    'numpy_func': numpy_name,
                    'status': 'FAILED',
                    'errors': error_messages[:3]  # Limit to first 3 errors
                })
    
    def test_rfx_functions(self):
        """Test all RFX submodule functions."""
        print("Testing rfx submodule functions...")
        
        if 'rfx' not in self.mappings:
            print("  No RFX mappings found, skipping...")
            return
            
        rfx_mappings = self.mappings['rfx']
        test_cases = self._get_test_cases()
        
        for numpy_name, zwc_name in rfx_mappings.items():
            # Skip reverse mappings
            if numpy_name in rfx_mappings.values():
                continue
                
            print(f"  Testing rfx.{zwc_name} -> numpy.linalg.{numpy_name}")
            
            # Get numpy function (most rfx functions are from linalg)
            if hasattr(np.linalg, numpy_name):
                numpy_func = getattr(np.linalg, numpy_name)
            elif hasattr(np, numpy_name):
                numpy_func = getattr(np, numpy_name)
            else:
                self.results['skipped'] += 1
                self.results['details'].append({
                    'function': f'rfx.{zwc_name}',
                    'numpy_func': f'linalg.{numpy_name}',
                    'status': 'SKIPPED',
                    'reason': f'numpy function not found'
                })
                continue
            
            # Get ZWC RFX function
            if not hasattr(self.zwc_rfx, zwc_name):
                self.results['errors'] += 1
                self.results['details'].append({
                    'function': f'rfx.{zwc_name}',
                    'numpy_func': f'linalg.{numpy_name}',
                    'status': 'ERROR',
                    'reason': f'zwc.rfx.{zwc_name} does not exist'
                })
                continue
                
            zwc_func = getattr(self.zwc_rfx, zwc_name)
            
            # Test with matrix-appropriate test cases
            matrix_cases = [tc for tc in test_cases if 'array_2d' in tc['name']]
            if not matrix_cases:
                matrix_cases = [{"name": "default_matrix", "data": [[1, 2], [3, 4]]}]
            
            function_passed = True
            error_messages = []
            
            for test_case in matrix_cases:
                args, kwargs = self._prepare_test_data(test_case, numpy_name)
                if args is None:
                    # Use default matrix for linalg functions
                    args = [[[1, 2], [3, 4]]]
                
                # Call both functions
                zwc_result, zwc_error = self._safe_call(zwc_func, args, kwargs)
                numpy_result, numpy_error = self._safe_call(numpy_func, args, kwargs)
                
                # Compare (similar logic to main functions)
                if zwc_error and numpy_error:
                    continue
                elif zwc_error and not numpy_error:
                    function_passed = False
                    error_messages.append(f"Test {test_case['name']}: ZWC error: {zwc_error}")
                    continue
                elif not zwc_error and numpy_error:
                    function_passed = False
                    error_messages.append(f"Test {test_case['name']}: Numpy error: {numpy_error}")
                    continue
                
                match, comparison_msg = self._compare_results(zwc_result, numpy_result, numpy_name)
                if not match:
                    function_passed = False
                    error_messages.append(f"Test {test_case['name']}: {comparison_msg}")
            
            # Record results
            if function_passed:
                self.results['passed'] += 1
                self.results['details'].append({
                    'function': f'rfx.{zwc_name}',
                    'numpy_func': f'linalg.{numpy_name}',
                    'status': 'PASSED'
                })
            else:
                self.results['failed'] += 1
                self.results['details'].append({
                    'function': f'rfx.{zwc_name}',
                    'numpy_func': f'linalg.{numpy_name}',
                    'status': 'FAILED',
                    'errors': error_messages[:3]
                })
    
    def generate_report(self):
        """Generate comprehensive test report."""
        total_tests = self.results['passed'] + self.results['failed'] + self.results['errors'] + self.results['skipped']
        
        print("\n" + "="*80)
        print("COMPREHENSIVE ZWC FUNCTION MAPPING TEST REPORT")
        print("="*80)
        print(f"Total functions tested: {total_tests}")
        print(f"✅ PASSED: {self.results['passed']}")
        print(f"❌ FAILED: {self.results['failed']}")
        print(f"💥 ERRORS: {self.results['errors']}")
        print(f"⏭️  SKIPPED: {self.results['skipped']}")
        
        if self.results['passed'] > 0:
            success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed'])) * 100
            print(f"📊 Success rate: {success_rate:.1f}%")
        
        # Detailed failure report
        failures = [d for d in self.results['details'] if d['status'] == 'FAILED']
        if failures:
            print(f"\n{'='*80}")
            print("DETAILED FAILURE ANALYSIS")
            print("="*80)
            for failure in failures:
                print(f"\n❌ {failure['function']} -> {failure['numpy_func']}")
                if 'errors' in failure:
                    for error in failure['errors']:
                        print(f"   • {error}")
        
        # Error report
        errors = [d for d in self.results['details'] if d['status'] == 'ERROR']
        if errors:
            print(f"\n{'='*80}")
            print("ERRORS (MISSING FUNCTIONS)")
            print("="*80)
            for error in errors:
                print(f"💥 {error['function']} -> {error['numpy_func']}: {error['reason']}")
        
        print(f"\n{'='*80}")
        print("TEST SUMMARY")
        print("="*80)
        if self.results['failed'] == 0 and self.results['errors'] == 0:
            print("🎉 ALL TESTS PASSED! Function mappings are correct.")
        else:
            print("⚠️  Some issues found. Review the detailed analysis above.")
        print("="*80)
    
    def run_all_tests(self):
        """Run the complete test suite."""
        print("Starting comprehensive ZWC function mapping tests...\n")
        
        self.test_main_functions()
        self.test_rfx_functions()
        self.generate_report()


if __name__ == "__main__":
    tester = ZWCTester()
    tester.run_all_tests()