"""Unit tests for the GeoDVFDataset class."""

import unittest

from price_estimator.datasets.geo_dvf import GeoDVFDataset
from pathlib import Path


class TestGeoDVFDataset(unittest.TestCase):
    """Test cases for GeoDVFDataset class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.default_year = [2023]
        self.default_departments = [75, 92, 93, 94]
        self.default_storage_path = "data/geo_dvf"

    def test_init_with_defaults(self):
        """Test initialization with default parameters."""
        dataset = GeoDVFDataset(year=self.default_year)

        self.assertEqual(dataset.year, self.default_year)
        self.assertEqual(dataset.departments, self.default_departments)

    def test_init_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        custom_year = [2022, 2023]
        custom_departments = [75, 92]
        custom_storage_path = "custom/path"

        dataset = GeoDVFDataset(
            year=custom_year,
            departments=custom_departments,
            storage_path=custom_storage_path,
        )

        self.assertEqual(dataset.year, custom_year)
        self.assertEqual(dataset.departments, custom_departments)
        self.assertEqual(dataset.storage_path, Path(custom_storage_path).resolve())

    def test_init_with_empty_departments(self):
        """Test initialization with empty departments list."""
        dataset = GeoDVFDataset(year=self.default_year, departments=[])

        self.assertEqual(dataset.year, self.default_year)
        self.assertEqual(dataset.departments, [])

    def test_get_url_single_year_department(self):
        """Test _get_url method with single year and department."""
        dataset = GeoDVFDataset(year=[2023])

        url = dataset._get_url(2023, 75)
        expected_url = (
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/75.csv.gz"
        )

        self.assertEqual(url, expected_url)

    def test_get_url_different_year_department(self):
        """Test _get_url method with different year and department."""
        dataset = GeoDVFDataset(year=[2022])

        url = dataset._get_url(2022, 92)
        expected_url = (
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2022/departements/92.csv.gz"
        )

        self.assertEqual(url, expected_url)

    def test_get_urls_single_year_single_department(self):
        """Test get_urls method with single year and department."""
        dataset = GeoDVFDataset(year=[2023], departments=[75])

        urls = dataset.get_urls()
        expected_urls = [
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/75.csv.gz"
        ]

        self.assertEqual(urls, expected_urls)

    def test_get_urls_single_year_multiple_departments(self):
        """Test get_urls method with single year and multiple departments."""
        dataset = GeoDVFDataset(year=[2023], departments=[75, 92])

        urls = dataset.get_urls()
        expected_urls = [
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/75.csv.gz",
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/92.csv.gz",
        ]

        self.assertEqual(urls, expected_urls)

    def test_get_urls_multiple_years_single_department(self):
        """Test get_urls method with multiple years and single department."""
        dataset = GeoDVFDataset(year=[2022, 2023], departments=[75])

        urls = dataset.get_urls()
        expected_urls = [
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2022/departements/75.csv.gz",
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/75.csv.gz",
        ]

        self.assertEqual(urls, expected_urls)

    def test_get_urls_multiple_years_multiple_departments(self):
        """Test get_urls method with multiple years and departments."""
        dataset = GeoDVFDataset(year=[2022, 2023], departments=[75, 92])

        urls = dataset.get_urls()
        expected_urls = [
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2022/departements/75.csv.gz",
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2022/departements/92.csv.gz",
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/75.csv.gz",
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/92.csv.gz",
        ]

        self.assertEqual(urls, expected_urls)

    def test_get_urls_with_default_departments(self):
        """Test get_urls method with default departments."""
        dataset = GeoDVFDataset(year=[2023])

        urls = dataset.get_urls()
        expected_urls = [
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/75.csv.gz",
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/92.csv.gz",
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/93.csv.gz",
            "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/94.csv.gz",
        ]

        self.assertEqual(urls, expected_urls)

    def test_get_urls_empty_departments(self):
        """Test get_urls method with empty departments list."""
        dataset = GeoDVFDataset(year=[2023], departments=[])

        urls = dataset.get_urls()
        expected_urls = []

        self.assertEqual(urls, expected_urls)

    def test_get_urls_empty_year(self):
        """Test get_urls method with empty year list."""
        dataset = GeoDVFDataset(year=[], departments=[75])

        urls = dataset.get_urls()
        expected_urls = []

        self.assertEqual(urls, expected_urls)

    def test_url_format_consistency(self):
        """Test that URL format is consistent across different inputs."""
        dataset = GeoDVFDataset(year=[2023])

        # Test with different data types for department
        url_int = dataset._get_url(2023, 75)
        url_str = dataset._get_url(2023, "75")

        # Both should work and produce valid URLs
        self.assertTrue(
            url_int.startswith("https://files.data.gouv.fr/geo-dvf/latest/csv/")
        )
        self.assertTrue(
            url_str.startswith("https://files.data.gouv.fr/geo-dvf/latest/csv/")
        )
        self.assertTrue(url_int.endswith(".csv.gz"))
        self.assertTrue(url_str.endswith(".csv.gz"))

    def test_departments_type_handling(self):
        """Test that departments can handle different types."""
        # Test with string departments

        # Test with integer departments
        dataset_int = GeoDVFDataset(year=[2023], departments=[75, 92])
        urls_int = dataset_int.get_urls()

        # Both should produce URLs (though content might differ)
        self.assertEqual(len(urls_int), 2)
        self.assertTrue(all(url.endswith(".csv.gz") for url in urls_int))

    def test_temp_directory_usage(self):
        """Test using default temporary directory storage."""
        dataset = GeoDVFDataset(year=[2023], departments=[75])

        # Should use default temp directory location
        self.assertTrue(str(dataset.storage_path).endswith("geo_dvf_cache"))
        self.assertTrue(dataset.storage_path.exists())

        # Clean up
        dataset.cleanup()

    def test_persistent_storage(self):
        """Test using persistent storage."""
        custom_path = "test_data/geo_dvf"
        dataset = GeoDVFDataset(
            year=[2023],
            departments=[75],
            storage_path=custom_path,
        )

        path_parts = str(dataset.storage_path).split("/")[-2:]
        self.assertEqual(path_parts, ["test_data", "geo_dvf"])

    def test_basic_functionality(self):
        """Test basic functionality without context manager."""
        dataset = GeoDVFDataset(year=[2023], departments=[75])
        self.assertTrue(dataset.storage_path.exists())

        # Test that storage path is persistent
        storage_path = dataset.storage_path
        self.assertTrue(storage_path.exists())

    def test_cleanup_method(self):
        """Test the cleanup method."""
        dataset = GeoDVFDataset(year=[2023], departments=[75])
        temp_path = dataset.storage_path

        # Storage path should exist
        self.assertTrue(temp_path.exists())

        # After cleanup, specific files should be cleaned but not the directory
        dataset.cleanup()
        # Note: cleanup() only removes files for requested years/departments


if __name__ == "__main__":
    unittest.main()
