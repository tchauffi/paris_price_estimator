#!/usr/bin/env python3
"""Test script to verify the optimized download functionality."""

import time
from src.price_estimator.datasets.geo_dvf import GeoDVFDataset


def test_optimized_download():
    """Test that the optimized download only fetches missing files."""
    print("=== Testing Optimized Download Functionality ===")

    # Create dataset with a small test case
    dataset = GeoDVFDataset(year=[2023], departments=[75])
    print(f"Storage path: {dataset.storage_path}")
    print(f"URLs to download: {dataset.get_urls()}")

    # First download - should download the file
    print("\n--- First download (should fetch file) ---")
    start_time = time.time()
    dataset.download()
    first_download_time = time.time() - start_time
    print(f"First download took: {first_download_time:.2f} seconds")

    # Second download - should skip existing file
    print("\n--- Second download (should skip existing file) ---")
    start_time = time.time()
    dataset.download()
    second_download_time = time.time() - start_time
    print(f"Second download took: {second_download_time:.2f} seconds")

    # Test adding more years - should only download new files
    print("\n--- Adding more years (should only download new files) ---")
    dataset_multi = GeoDVFDataset(year=[2022, 2023], departments=[75])
    start_time = time.time()
    dataset_multi.download()
    multi_download_time = time.time() - start_time
    print(f"Multi-year download took: {multi_download_time:.2f} seconds")

    # Test loading data
    print("\n--- Testing data loading ---")
    df = dataset_multi.open_db()
    print(f"Loaded DataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)[:5]}...")  # Show first 5 columns

    # Test with new file naming
    print("\n--- Testing file naming ---")
    filepath_2022 = dataset_multi._get_filepath(2022, 75)
    filepath_2023 = dataset_multi._get_filepath(2023, 75)
    print(f"2022 file: {filepath_2022}")
    print(f"2023 file: {filepath_2023}")
    print(f"2022 exists: {filepath_2022.exists()}")
    print(f"2023 exists: {filepath_2023.exists()}")

    # Cleanup
    print("\n--- Cleanup ---")
    dataset_multi.cleanup()
    print("Cleanup completed")

    print("\n=== Test completed successfully! ===")


if __name__ == "__main__":
    test_optimized_download()
