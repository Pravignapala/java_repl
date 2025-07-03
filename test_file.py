#!/usr/bin/env python3
"""
Test suite for package_sorter.py

Comprehensive unit tests for the package sorting system.
"""

import unittest
import sys
from package_sorter import sort


class TestPackageSorter(unittest.TestCase):
    """Test cases for the package sorting function."""

    def test_standard_packages(self):
        """Test packages that should be classified as STANDARD."""
        test_cases = [
            (10, 10, 10, 5, "Small standard package"),
            (50, 50, 50, 10, "Medium standard package"),
            (100, 100, 99, 19, "Large but not bulky/heavy"),
            (149, 149, 149, 19.9, "Just under thresholds"),
            (0, 0, 0, 0, "Zero dimensions and mass"),
            (1, 1, 1, 1, "Minimal package"),
        ]
        
        for width, height, length, mass, description in test_cases:
            with self.subTest(description=description):
                result = sort(width, height, length, mass)
                self.assertEqual(result, "STANDARD",
                    f"Failed for {description}: w={width}, h={height}, l={length}, m={mass}")

    def test_heavy_only_packages(self):
        """Test packages that are heavy but not bulky (should be SPECIAL)."""
        test_cases = [
            (10, 10, 10, 20, "Heavy but not bulky - exact threshold"),
            (50, 50, 50, 25, "Heavy medium package"),
            (100, 100, 99, 30, "Heavy large package"),
            (10, 10, 10, 100, "Very heavy small package"),
            (149, 149, 149, 20, "Heavy, just under bulky threshold"),
        ]
        
        for width, height, length, mass, description in test_cases:
            with self.subTest(description=description):
                result = sort(width, height, length, mass)
                self.assertEqual(result, "SPECIAL",
                    f"Failed for {description}: w={width}, h={height}, l={length}, m={mass}")

    def test_bulky_by_volume_packages(self):
        """Test packages that are bulky by volume but not heavy (should be SPECIAL)."""
        test_cases = [
            (100, 100, 100, 5, "Bulky by volume, not heavy"),
            (200, 200, 25, 10, "Bulky by volume, medium weight"),
            (1000, 1000, 1, 15, "Very bulky by volume"),
            (100, 100, 100, 19, "Bulky by volume, just under heavy threshold"),
        ]
        
        for width, height, length, mass, description in test_cases:
            with self.subTest(description=description):
                result = sort(width, height, length, mass)
                self.assertEqual(result, "SPECIAL",
                    f"Failed for {description}: w={width}, h={height}, l={length}, m={mass}")

    def test_bulky_by_dimension_packages(self):
        """Test packages that are bulky by single dimension but not heavy (should be SPECIAL)."""
        test_cases = [
            (150, 10, 10, 5, "Bulky by width - exact threshold"),
            (10, 150, 10, 5, "Bulky by height - exact threshold"),
            (10, 10, 150, 5, "Bulky by length - exact threshold"),
            (200, 50, 50, 15, "Bulky by dimension, not heavy"),
            (300, 1, 1, 1, "Very long thin package"),
            (1, 200, 1, 1, "Very tall thin package"),
            (1, 1, 500, 1, "Very long thin package"),
        ]
        
        for width, height, length, mass, description in test_cases:
            with self.subTest(description=description):
                result = sort(width, height, length, mass)
                self.assertEqual(result, "SPECIAL",
                    f"Failed for {description}: w={width}, h={height}, l={length}, m={mass}")

    def test_rejected_packages(self):
        """Test packages that are both heavy and bulky (should be REJECTED)."""
        test_cases = [
            (150, 10, 10, 20, "Heavy and bulky by dimension"),
            (100, 100, 100, 25, "Heavy and bulky by volume"),
            (200, 200, 25, 30, "Heavy and bulky by both"),
            (150, 150, 150, 50, "Very heavy and very bulky"),
            (150, 150, 150, 20, "Exactly at both thresholds"),
            (1000, 1000, 1, 100, "Extremely bulky and heavy"),
        ]
        
        for width, height, length, mass, description in test_cases:
            with self.subTest(description=description):
                result = sort(width, height, length, mass)
                self.assertEqual(result, "REJECTED",
                    f"Failed for {description}: w={width}, h={height}, l={length}, m={mass}")

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test exact thresholds
        self.assertEqual(sort(149.9, 149.9, 149.9, 19.9), "STANDARD")
        self.assertEqual(sort(150, 1, 1, 1), "SPECIAL")
        self.assertEqual(sort(1, 150, 1, 1), "SPECIAL")
        self.assertEqual(sort(1, 1, 150, 1), "SPECIAL")
        self.assertEqual(sort(1, 1, 1, 20), "SPECIAL")
        self.assertEqual(sort(150, 1, 1, 20), "REJECTED")
        
        # Test volume exactly at threshold
        self.assertEqual(sort(100, 100, 100, 19), "SPECIAL")  # Volume = 1,000,000
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")  # Volume = 1,000,000 and heavy
        
        # Test floating point precision
        self.assertEqual(sort(99.9, 99.9, 100.1, 19.9), "STANDARD")
        self.assertEqual(sort(100.0, 100.0, 100.0, 20.0), "REJECTED")

    def test_input_validation_negative_values(self):
        """Test that negative values raise ValueError."""
        with self.assertRaises(ValueError):
            sort(-1, 10, 10, 5)
        
        with self.assertRaises(ValueError):
            sort(10, -1, 10, 5)
        
        with self.assertRaises(ValueError):
            sort(10, 10, -1, 5)
        
        with self.assertRaises(ValueError):
            sort(10, 10, 10, -1)

    def test_input_validation_non_numeric(self):
        """Test that non-numeric inputs raise TypeError."""
        with self.assertRaises(TypeError):
            sort("abc", 10, 10, 5)
        
        with self.assertRaises(TypeError):
            sort(10, "xyz", 10, 5)
        
        with self.assertRaises(TypeError):
            sort(10, 10, "def", 5)
        
        with self.assertRaises(TypeError):
            sort(10, 10, 10, "heavy")
        
        with self.assertRaises(TypeError):
            sort(None, 10, 10, 5)
        
        with self.assertRaises(TypeError):
            sort(10, 10, 10, None)

    def test_string_numeric_inputs(self):
        """Test that string representations of numbers are handled correctly."""
        # These should work (string numbers should be converted)
        self.assertEqual(sort("10", "10", "10", "5"), "STANDARD")
        self.assertEqual(sort("150", "10", "10", "5"), "SPECIAL")
        self.assertEqual(sort("10", "10", "10", "20"), "SPECIAL")
        self.assertEqual(sort("150", "10", "10", "20"), "REJECTED")

    def test_float_inputs(self):
        """Test that float inputs work correctly."""
        self.assertEqual(sort(10.5, 10.5, 10.5, 5.5), "STANDARD")
        self.assertEqual(sort(149.9, 149.9, 149.9, 19.9), "STANDARD")
        self.assertEqual(sort(150.1, 10.0, 10.0, 5.0), "SPECIAL")
        self.assertEqual(sort(10.0, 10.0, 10.0, 20.1), "SPECIAL")

    def test_large_numbers(self):
        """Test handling of very large numbers."""
        # Very large dimensions
        self.assertEqual(sort(10000, 10000, 10000, 5), "SPECIAL")
        self.assertEqual(sort(10000, 10000, 10000, 100), "REJECTED")
        
        # Very large mass
        self.assertEqual(sort(10, 10, 10, 1000), "SPECIAL")
        self.assertEqual(sort(200, 10, 10, 1000), "REJECTED")

    def test_performance_stress(self):
        """Test that the function performs well with many calls."""
        import time
        
        start_time = time.time()
        for i in range(10000):
            sort(i % 200, i % 200, i % 200, i % 50)
        end_time = time.time()
        
        # Should complete 10,000 operations in well under 1 second
        self.assertLess(end_time - start_time, 1.0, 
                       "Function should handle 10,000 operations quickly")


def run_performance_benchmark():
    """Run a performance benchmark of the sorting function."""
    import time
    
    print("\n" + "="*50)
    print("PERFORMANCE BENCHMARK")
    print("="*50)
    
    # Test different package types
    test_scenarios = [
        ("Standard packages", [(50, 50, 50, 10)] * 10000),
        ("Heavy packages", [(50, 50, 50, 25)] * 10000),
        ("Bulky packages", [(150, 50, 50, 10)] * 10000),
        ("Rejected packages", [(150, 50, 50, 25)] * 10000),
        ("Mixed packages", [(50, 50, 50, 10), (150, 50, 50, 10), 
                           (50, 50, 50, 25), (150, 50, 50, 25)] * 2500),
    ]
    
    for scenario_name, packages in test_scenarios:
        start_time = time.time()
        for width, height, length, mass in packages:
            sort(width, height, length, mass)
        end_time = time.time()
        
        elapsed = end_time - start_time
        packages_per_second = len(packages) / elapsed
        
        print(f"{scenario_name}:")
        print(f"  Processed {len(packages):,} packages in {elapsed:.4f} seconds")
        print(f"  Rate: {packages_per_second:,.0f} packages/second")
        print()


if __name__ == "__main__":
    # Run the tests
    unittest.main(verbosity=2, exit=False)
    
    # Run performance benchmark
    run_performance_benchmark()
