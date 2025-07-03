#!/usr/bin/env python3
"""
Thoughtful Robotic Automation Factory - Package Sorting System

This module implements a package sorting function that categorizes packages
based on their dimensions and mass into appropriate handling stacks.

Author: Solution for Technical Screen
"""

def sort(width, height, length, mass):
    """
    Sort packages into appropriate stacks based on volume and mass criteria.
    
    Args:
        width (float): Package width in centimeters
        height (float): Package height in centimeters  
        length (float): Package length in centimeters
        mass (float): Package mass in kilograms
    
    Returns:
        str: Stack name where package should be dispatched
             - "STANDARD": Normal packages (not bulky or heavy)
             - "SPECIAL": Heavy OR bulky packages
             - "REJECTED": Heavy AND bulky packages
    
    Raises:
        ValueError: If any dimension or mass is negative
        TypeError: If inputs are not numeric
    """
    # Input validation
    try:
        width = float(width)
        height = float(height)
        length = float(length)
        mass = float(mass)
    except (ValueError, TypeError):
        raise TypeError("All inputs must be numeric")
    
    if width < 0 or height < 0 or length < 0 or mass < 0:
        raise ValueError("Dimensions and mass must be non-negative")
    
    # Calculate volume
    volume = width * height * length
    
    # Determine if package is bulky
    is_bulky = (volume >= 1_000_000 or 
                width >= 150 or 
                height >= 150 or 
                length >= 150)
    
    # Determine if package is heavy
    is_heavy = mass >= 20
    
    # Sort into appropriate stack
    if is_heavy and is_bulky:
        return "REJECTED"
    elif is_heavy or is_bulky:
        return "SPECIAL"
    else:
        return "STANDARD"


# Test Cases
def run_tests():
    """Comprehensive test suite for the sort function."""
    
    test_cases = [
        # (width, height, length, mass, expected_result, description)
        
        # STANDARD cases
        (10, 10, 10, 5, "STANDARD", "Small standard package"),
        (50, 50, 50, 10, "STANDARD", "Medium standard package"),
        (100, 100, 99, 19, "STANDARD", "Large but not bulky/heavy"),
        (149, 149, 149, 19.9, "STANDARD", "Just under thresholds"),
        
        # SPECIAL cases - Heavy only
        (10, 10, 10, 20, "SPECIAL", "Heavy but not bulky"),
        (50, 50, 50, 25, "SPECIAL", "Heavy medium package"),
        (100, 100, 99, 30, "SPECIAL", "Heavy large package"),
        
        # SPECIAL cases - Bulky by volume
        (100, 100, 100, 5, "SPECIAL", "Bulky by volume, not heavy"),
        (200, 200, 25, 10, "SPECIAL", "Bulky by volume, medium weight"),
        
        # SPECIAL cases - Bulky by dimension
        (150, 10, 10, 5, "SPECIAL", "Bulky by width"),
        (10, 150, 10, 5, "SPECIAL", "Bulky by height"),
        (10, 10, 150, 5, "SPECIAL", "Bulky by length"),
        (200, 50, 50, 15, "SPECIAL", "Bulky by dimension, not heavy"),
        
        # REJECTED cases
        (150, 10, 10, 20, "REJECTED", "Heavy and bulky by dimension"),
        (100, 100, 100, 25, "REJECTED", "Heavy and bulky by volume"),
        (200, 200, 25, 30, "REJECTED", "Heavy and bulky by both"),
        (150, 150, 150, 50, "REJECTED", "Very heavy and very bulky"),
        
        # Edge cases
        (0, 0, 0, 0, "STANDARD", "Zero dimensions and mass"),
        (149.9, 149.9, 149.9, 19.9, "STANDARD", "Just under all thresholds"),
        (150, 150, 150, 20, "REJECTED", "Exactly at both thresholds"),
        (1, 1, 1000000, 1, "SPECIAL", "Bulky by volume with minimal other dims"),
    ]
    
    print("Running Package Sorting Tests...")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for width, height, length, mass, expected, description in test_cases:
        try:
            result = sort(width, height, length, mass)
            if result == expected:
                print(f"✓ PASS: {description}")
                print(f"  Input: w={width}, h={height}, l={length}, m={mass}")
                print(f"  Result: {result}")
                passed += 1
            else:
                print(f"✗ FAIL: {description}")
                print(f"  Input: w={width}, h={height}, l={length}, m={mass}")
                print(f"  Expected: {expected}, Got: {result}")
                failed += 1
        except Exception as e:
            print(f"✗ ERROR: {description}")
            print(f"  Exception: {e}")
            failed += 1
        print()
    
    # Test error cases
    print("Testing Error Handling...")
    print("-" * 30)
    
    error_cases = [
        ((-1, 10, 10, 5), ValueError, "Negative width"),
        ((10, -1, 10, 5), ValueError, "Negative height"),
        ((10, 10, -1, 5), ValueError, "Negative length"),
        ((10, 10, 10, -1), ValueError, "Negative mass"),
        (("abc", 10, 10, 5), TypeError, "Non-numeric width"),
        ((10, "xyz", 10, 5), TypeError, "Non-numeric height"),
        ((None, 10, 10, 5), TypeError, "None input"),
    ]
    
    for inputs, expected_error, description in error_cases:
        try:
            sort(*inputs)
            print(f"✗ FAIL: {description} - Should have raised {expected_error.__name__}")
            failed += 1
        except expected_error:
            print(f"✓ PASS: {description} - Correctly raised {expected_error.__name__}")
            passed += 1
        except Exception as e:
            print(f"✗ FAIL: {description} - Wrong exception type: {type(e).__name__}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print(f"Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    return failed == 0


# Example usage and demonstration
def demonstrate_sorting():
    """Demonstrate the sorting function with various package examples."""
    
    print("Package Sorting Demonstration")
    print("=" * 40)
    
    examples = [
        (50, 50, 50, 10, "Standard shipping box"),
        (200, 50, 50, 15, "Long tube - bulky by dimension"),
        (80, 80, 80, 25, "Heavy equipment box"),
        (100, 100, 100, 30, "Heavy and bulky - industrial equipment"),
        (149, 149, 149, 19, "Large but within limits"),
        (150, 1, 1, 1, "Thin rod - bulky by single dimension"),
    ]
    
    for width, height, length, mass, description in examples:
        result = sort(width, height, length, mass)
        volume = width * height * length
        
        print(f"\nPackage: {description}")
        print(f"Dimensions: {width}×{height}×{length} cm")
        print(f"Volume: {volume:,} cm³")
        print(f"Mass: {mass} kg")
        print(f"Classification: {result}")
        
        # Show reasoning
        is_bulky = volume >= 1_000_000 or max(width, height, length) >= 150
        is_heavy = mass >= 20
        
        reasons = []
        if is_bulky:
            if volume >= 1_000_000:
                reasons.append("volume ≥ 1,000,000 cm³")
            if max(width, height, length) >= 150:
                reasons.append("dimension ≥ 150 cm")
        if is_heavy:
            reasons.append("mass ≥ 20 kg")
        
        if reasons:
            print(f"Reason: {' and '.join(reasons)}")
        else:
            print("Reason: within standard limits")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_sorting()
    print("\n" + "=" * 60 + "\n")
    
    # Run comprehensive tests
    success = run_tests()
    
    if success:
        print("\n🎉 All tests passed! The sorting function is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please review the implementation.")
