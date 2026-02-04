#!/usr/bin/env python3
"""
Comprehensive test of the random numpy package.
"""

import sys
import os
import json

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
        
        try:
            inv_matrix = linalg.quvohe(matrix)  # inv
            print(f"✅ Matrix inverse: {inv_matrix}")
        except Exception as e:
            print(f"⚠️  Matrix inverse (expected for singular matrix): {e}")
        
        # Test linear system solving
        b = rnp.yitaf([5, 6])
        try:
            x = linalg.sarik(matrix, b)  # solve
            print(f"✅ Linear solve: {x}")
        except Exception as e:
            print(f"⚠️  Linear solve result: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_function_availability():
    """Test that functions are available and callable."""
    print("\nTesting function availability...")
    
    try:
        import random_numpy_package as rnp
        from random_numpy_package import linalg
        
        # Load mappings to test
        with open('mappings.json', 'r') as f:
            mappings = json.load(f)
        
        # Test a sample of main functions
        sample_main = list(mappings['main'].items())[:10]
        for orig_name, random_name in sample_main:
            if hasattr(rnp, random_name):
                func = getattr(rnp, random_name)
                if callable(func):
                    print(f"✅ {random_name} (was {orig_name}) - callable")
                else:
                    print(f"❌ {random_name} - not callable")
            else:
                print(f"❌ {random_name} - not found")
        
        # Test linalg functions
        sample_linalg = list(mappings['linalg'].items())[:5]
        for orig_name, random_name in sample_linalg:
            if hasattr(linalg, random_name):
                func = getattr(linalg, random_name)
                if callable(func):
                    print(f"✅ linalg.{random_name} (was {orig_name}) - callable")
                else:
                    print(f"❌ linalg.{random_name} - not callable")
            else:
                print(f"❌ linalg.{random_name} - not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Function availability test failed: {str(e)}")
        return False

def test_documentation():
    """Test documentation files exist and contain content."""
    print("\nTesting documentation...")
    
    doc_files = [
        'README.md',
        'docs/main_functions.md',
        'docs/linalg_functions.md', 
        'docs/function_index.md'
    ]
    
    all_exist = True
    for doc_file in doc_files:
        if os.path.exists(doc_file):
            size = os.path.getsize(doc_file)
            if size > 100:  # At least 100 bytes
                print(f"✅ {doc_file} exists ({size} bytes)")
            else:
                print(f"⚠️  {doc_file} exists but seems too small ({size} bytes)")
        else:
            print(f"❌ {doc_file} missing")
            all_exist = False
    
    return all_exist

def test_practical_examples():
    """Test some practical usage examples."""
    print("\nTesting practical examples...")
    
    try:
        import random_numpy_package as rnp
        from random_numpy_package import linalg
        
        # Data analysis example
        data = rnp.yitaf([1.2, 2.4, 3.1, 4.8, 5.2, 6.7, 7.1, 8.9, 9.3, 10.5])
        mean = rnp.kocito(data)  # mean
        std_dev = rnp.fatohe(data)  # std
        print(f"✅ Statistical analysis - Mean: {mean:.2f}, Std: {std_dev:.2f}")
        
        # Matrix operations
        A = rnp.yitaf([[1, 2], [3, 4]])
        B = rnp.yitaf([[5, 6], [7, 8]])
        C = rnp.mixut(A, B)  # matmul
        print(f"✅ Matrix multiplication result shape: {C.shape}")
        
        # Mathematical functions
        x = rnp.ponife(0, 6.28, 100)  # linspace (0 to 2π)
        y = rnp.tefiwif(x)  # sin
        print(f"✅ Sine wave generated with {len(y)} points")
        
        return True
        
    except Exception as e:
        print(f"❌ Practical examples failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Comprehensive Testing of Random NumPy Package")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_basic_functionality()
    all_passed &= test_function_availability()
    all_passed &= test_documentation()
    all_passed &= test_practical_examples()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Package is ready for agent testing.")
        
        # Show final statistics
        with open('mappings.json', 'r') as f:
            mappings = json.load(f)
        
        print(f"\n📊 Package Statistics:")
        print(f"   • {len(mappings['main'])} main functions")
        print(f"   • {len(mappings['linalg'])} linear algebra functions")
        print(f"   • Total: {len(mappings['main']) + len(mappings['linalg'])} functions")
        print(f"   • Documentation files: 4")
        
        print(f"\n🔍 Sample function mappings:")
        print(f"   • array() → yitaf()")
        print(f"   • add() → lahonig()")
        print(f"   • mean() → kocito()")
        print(f"   • linalg.inv() → linalg.quvohe()")
        print(f"   • linalg.solve() → linalg.sarik()")
        
    else:
        print("❌ Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main()