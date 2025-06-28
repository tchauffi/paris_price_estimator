"""This module contains the dataset Geo DVF dataset class."""

from __future__ import annotations


class GeoDVFDataset:
    """Dataset class for Geo DVF dataset."""

    def __init__(
        self,
        year: list[int],
        departments: list[int] = [75, 92, 93, 94],
        storage_path: str = "data/geo_dvf",
        dataset_url: str = "https://files.data.gouv.fr/geo-dvf/latest/csv",
    ):
        """Initialize the GeoDVFDataset.

        Args:
            year (int): The year of the dataset.
            departments (list[str], optional): List of departments to filter.
            Defaults to IdF departments.
            storage_path (str, optional): Path to store the dataset.
                Defaults to "data/geo_dvf".
            dataset_url (str, optional): Base URL for the Geo DVF dataset.
                Defaults to "https://files.data.gouv.fr/geo-dvf/latest/csv".

        Raises:
            ValueError: If year is not a list of integers or if departments is
            not a list of integers.
            ValueError: If any element in year or departments is not an
            integer.
        """
        self.url = dataset_url
        if not isinstance(year, list):
            raise ValueError("Year must be a list of integers.")
        if not all(isinstance(y, int) for y in year):
            raise ValueError("All elements in year must be integers.")
        if not isinstance(departments, list):
            raise ValueError("Departments must be a list of integers.")
        if not all(isinstance(d, int) for d in departments):
            raise ValueError("All elements in departments must be integers.")

        self.url = dataset_url
        self.year = year
        self.departments = departments if departments else []
        self.storage_path = storage_path

    def _get_url(self, year, department) -> str:
        """Get the URL for the Geo DVF dataset.

        Returns:
            str: The URL for the Geo DVF dataset.
        """
        return f"{self.url}/{year}/departements/{department}.csv.gz"

    def get_urls(self) -> list[str]:
        """Get the URLs for the Geo DVF dataset.

        Returns:
            list[str]: List of URLs for the Geo DVF dataset.
        """
        urls = [
            self._get_url(year, department)
            for year in self.year
            for department in self.departments
        ]
        return urls
