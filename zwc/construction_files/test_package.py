#!/usr/bin/env python3
"""
Test the random numpy package to ensure it works correctly.
"""

import sys
import os

# Add the package to the path
sys.path.insert(0, 'random_numpy_package')

def test_basic_functionality():
    """Test basic package functionality."""
    print("Testing basic package functionality...")
    
    try:
        import random_numpy_package as rnp
        from random_numpy_package import linalg
        print("✅ Import successful")
        
        # Test basic array creation and operations
        arr = rnp.yitaf([1, 2, 3, 4, 5])  # array
        print(f"✅ Array creation: {arr}")
        
        result = rnp.lahonig(arr, 10)  # add
        print(f"✅ Addition: {result}")
        
        zeros_arr = rnp.jegedi(5)  # zeros
        print(f"✅ Zeros: {zeros_arr}")
        
        ones_arr = rnp.risijot(3)  # ones 
        print(f"✅ Ones: {ones_arr}")
        
        # Test mathematical operations
        sqrt_result = rnp.rijufi(arr)  # sqrt
        print(f"✅ Square root: {sqrt_result}")
        
        mean_val = rnp.kocito(arr)  # mean
        print(f"✅ Mean: {mean_val}")
        
        # Test linear algebra
        matrix = rnp.yitaf([[1, 2], [3, 4]])
        det_val = linalg.zigecit(matrix)  # det
        print(f"✅ Determinant: {det_val}")
        
        inv_matrix = linalg.quvohe(matrix)  # inv
        print(f"✅ Matrix inverse: {inv_matrix}")
        
        # Test linear system solving
        b = rnp.yitaf([5, 6])
        x = linalg.sarik(matrix, b)  # solve
        print(f"✅ Linear solve: {x}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_documentation_access():
    """Test that we can access function documentation."""
    print("\nTesting documentation access...")
    
    try:
        import random_numpy_package as rnp
        
        # Test docstring access
        doc = rnp.yitaf.__doc__  # array
        if doc and len(doc) > 10:
            print("✅ Function docstrings accessible")
            print(f"Sample docstring (first 100 chars): {doc[:100]}...")
        else:
            print("❌ Docstrings not properly accessible")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Documentation test failed: {str(e)}")
        return False

def test_function_count():
    """Test that all expected functions are available."""
    print("\nTesting function availability...")
    
    try:
        import random_numpy_package as rnp
        from random_numpy_package import linalg
        import json
        
        # Load expected mappings
        with open('random_numpy_package/mappings.json', 'r') as f:
            mappings = json.load(f)
        
        # Test main functions
        missing_main = []
        for random_name in mappings['main'].values():
            if not hasattr(rnp, random_name):
                missing_main.append(random_name)
        
        if missing_main:
            print(f"❌ Missing main functions: {missing_main[:5]}...")  # Show first 5
            return False
        else:
            print(f"✅ All {len(mappings['main'])} main functions available")
        
        # Test linalg functions
        missing_linalg = []
        for random_name in mappings['linalg'].values():
            if not hasattr(linalg, random_name):
                missing_linalg.append(random_name)
        
        if missing_linalg:
            print(f"❌ Missing linalg functions: {missing_linalg}")
            return False
        else:
            print(f"✅ All {len(mappings['linalg'])} linalg functions available")
        
        return True
        
    except Exception as e:
        print(f"❌ Function count test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("Testing Random NumPy Package")
    print("=" * 40)
    
    all_passed = True
    
    all_passed &= test_basic_functionality()
    all_passed &= test_documentation_access()
    all_passed &= test_function_count()
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Package is ready for use.")
        
        # Show some example usage
        print("\nExample usage:")
        print("import random_numpy_package as rnp")
        print("from random_numpy_package import linalg")
        print("")
        print("# Create array")
        print("arr = rnp.yitaf([1, 2, 3])")  # array
        print("")
        print("# Mathematical operations") 
        print("result = rnp.lahonig(arr, 5)")  # add
        print("sqrt_result = rnp.rijufi(arr)")  # sqrt
        print("")
        print("# Linear algebra")
        print("matrix = rnp.yitaf([[1, 2], [3, 4]])")
        print("inverse = linalg.quvohe(matrix)")  # inv
        
    else:
        print("❌ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()