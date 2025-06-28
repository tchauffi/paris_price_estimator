"""This module contains the dataset Geo DVF dataset class."""

from __future__ import annotations
from pathlib import Path
import pandas as pd
import requests
import tempfile


class GeoDVFDataset:
    """Dataset class for Geo DVF dataset."""

    def __init__(
        self,
        year: list[int],
        departments: list[int] = [75, 92, 93, 94],
        storage_path: str | None = None,
        dataset_url: str = "https://files.data.gouv.fr/geo-dvf/latest/csv",
    ):
        """Initialize the GeoDVFDataset.

        Args:
            year (list[int]): List of years for the dataset.
            departments (list[int], optional): List of departments to filter.
                Defaults to IdF departments.
            storage_path (str, optional): Path to store the dataset.
                If None, uses a persistent temp directory.
            dataset_url (str, optional): Base URL for the Geo DVF dataset.
                Defaults to "https://files.data.gouv.fr/geo-dvf/latest/csv".

        Raises:
            ValueError: If year is not a list of integers or if departments is
                not a list of integers.
            ValueError: If any element in year or departments is not an
                integer.
        """
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

        # Determine storage path - default to persistent temp directory
        if storage_path is None:
            temp_base = Path(tempfile.gettempdir()) / "geo_dvf_cache"
            self.storage_path = temp_base
        else:
            self.storage_path = Path(storage_path).resolve()

        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_filename(self, year: int, department: int) -> str:
        """Get the filename for a specific year and department.

        Args:
            year: The year of the dataset.
            department: The department code.

        Returns:
            str: The filename for the dataset file.
        """
        return f"{department}.csv.gz"

    def _get_filepath(self, year: int, department: int) -> Path:
        """Get the full filepath for a specific year and department.

        Args:
            year: The year of the dataset.
            department: The department code.

        Returns:
            Path: The full filepath for the dataset file.
        """
        filename = self._get_filename(year, department)
        return self.storage_path / f"{year}_{filename}"

    def _get_url(self, year: int, department: int) -> str:
        """Get the URL for the Geo DVF dataset.

        Args:
            year: The year of the dataset.
            department: The department code.

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

    def download(self) -> None:
        """Download only missing Geo DVF dataset files.

        This method checks which files are already present and only downloads
        the missing ones, optimizing download time and bandwidth usage.

        Raises:
            RuntimeError: If any download fails with a non-200 status code.
        """
        downloaded_count = 0
        skipped_count = 0

        for year in self.year:
            for department in self.departments:
                filepath = self._get_filepath(year, department)

                # Skip if file already exists
                if filepath.exists():
                    skipped_count += 1
                    print(f"Skipping {filepath.name} (already exists)")
                    continue

                # Download the file
                url = self._get_url(year, department)
                print(f"Downloading {filepath.name}...")

                response = requests.get(url)
                if response.status_code == 200:
                    with open(filepath, "wb") as file:
                        file.write(response.content)
                    downloaded_count += 1
                    print(f"Downloaded {filepath.name}")
                else:
                    raise RuntimeError(
                        f"Failed to download {url}: {response.status_code}"
                    )

        print(
            f"Download complete: {downloaded_count} new files, "
            f"{skipped_count} existing files"
        )

    def open_db(self) -> pd.DataFrame:
        """Open the Geo DVF dataset as a pandas DataFrame.

        Returns:
            pd.DataFrame: Concatenated DataFrame of all downloaded files.

        Raises:
            FileNotFoundError: If no dataset files found in storage path.
        """
        # Get files for the requested years and departments
        files = []
        for year in self.year:
            for department in self.departments:
                filepath = self._get_filepath(year, department)
                if filepath.exists():
                    files.append(filepath)

        if not files:
            raise FileNotFoundError(
                f"No dataset files found in {self.storage_path}. "
                "Did you run download() first?"
            )

        # Concatenate all CSV files into a single DataFrame
        df = pd.concat(
            (pd.read_csv(file, compression="gzip") for file in files), ignore_index=True
        )
        return df

    def cleanup(self) -> None:
        """Clean up downloaded files to free disk space."""
        files = [
            self._get_filepath(year, department)
            for year in self.year
            for department in self.departments
            if self._get_filepath(year, department).exists()
        ]

        for file in files:
            file.unlink()
        print(f"Cleaned up {len(files)} files from {self.storage_path}")


if __name__ == "__main__":
    # Example 1: Basic usage with default temp storage
    print("=== Example 1: Basic usage with default temp storage ===")
    dataset = GeoDVFDataset(year=[2023], departments=[75])
    print("Dataset URLs:", dataset.get_urls())
    print("Storage path:", dataset.storage_path)
    dataset.download()
    print("Download completed to:", dataset.storage_path)

    df = dataset.open_db()
    print("DataFrame shape:", df.shape)
    print("DataFrame columns:", df.columns.tolist()[:5])  # Show first 5 columns
    print()

    # Example 2: Multiple years and departments
    print("=== Example 2: Multiple years and departments ===")
    dataset_multi = GeoDVFDataset(year=[2022, 2023], departments=[75, 92])
    print(f"Will download {len(dataset_multi.get_urls())} files")
    dataset_multi.download()  # Only missing files will be downloaded
    df_multi = dataset_multi.open_db()
    print(f"Multi-year data shape: {df_multi.shape}")
    print()

    # Example 3: Custom storage path
    print("=== Example 3: Custom storage path ===")
    custom_dataset = GeoDVFDataset(
        year=[2023], departments=[75], storage_path="data/custom_geo_dvf"
    )
    print("Custom storage path:", custom_dataset.storage_path)
    custom_dataset.download()
    print("Files will persist in the custom directory!")
    print("Remember to use cleanup() if you want to free disk space later.")
