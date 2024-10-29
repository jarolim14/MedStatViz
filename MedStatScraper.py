import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


class MedStatScraper:
    """
    A class to scrape and parse statistical data from a specified URL.

    This class fetches HTML content from the given URL, parses a specific
    statistical data table, and formats the data into a pandas DataFrame.

    Attributes:
        url (str): The URL to scrape data from.
        html (str): The HTML content fetched from the URL.
        table_data (list): The parsed table data from the HTML.
        dataframe (pd.DataFrame): The formatted DataFrame containing the statistical data.

    Methods:
        fetch_html() -> None:
            Fetches the HTML content from the specified URL.

        parse_table() -> None:
            Parses the statistical data table from the fetched HTML content.

        format_dataframe() -> pd.DataFrame:
            Formats the parsed table data into a pandas DataFrame, including
            cleaning and converting data to numeric types, and adding metadata.

    Raises:
        ValueError: If the HTML content is not fetched, if no table is found,
                     or if the table data does not contain at least 3 rows.
        Exception: If the URL fetching fails due to a network issue.
    """

    def __init__(self, url: str):
        self.url = url
        self.html: str = None
        self.table_data: list = None
        self.dataframe: pd.DataFrame = None

    def fetch_html(self) -> None:
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad responses
            self.html = response.text
        except RequestException as e:
            raise Exception(f"Failed to fetch URL: {self.url}. Error: {e}")

    def parse_table(self) -> None:
        if self.html is None:
            raise ValueError("HTML content not fetched. Call fetch_html() first.")

        soup = BeautifulSoup(self.html, "html.parser")
        table = soup.find("table", class_="statistical-data-table")
        if not table:
            raise ValueError("No table found in the HTML content.")

        tr_elements = table.find_all("tr")
        self.table_data = [
            [cell.get_text(strip=True) for cell in tr if cell.get_text(strip=True)]
            for tr in tr_elements
        ]

    def format_dataframe(self) -> pd.DataFrame:
        if not self.table_data or len(self.table_data) < 3:
            raise ValueError("Table data must contain at least 3 rows")

        year_cols = self.table_data[0]
        setting = self.table_data[1][0]
        atc_codes = [row[0] for row in self.table_data[2:]]

        is_ddd = any("DDD" in str(row) for row in self.table_data[3:4])
        data_start_idx = 2 if is_ddd else 1
        unit = "DDD" if is_ddd else "Sales"

        data = [row[data_start_idx:] for row in self.table_data[2:]]

        df = pd.DataFrame(data, columns=year_cols)

        df = df.replace(
            {
                "-": np.nan,
                "": np.nan,
                r"[^0-9.]": "",  # Remove any non-numeric characters except decimal points
            },
            regex=True,
        )

        numeric_cols = df.columns
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        # remove empty columns
        # Find year columns where all values are NaN
        empty_years = [col for col in year_cols if df[col].isna().all()]
        # Drop those columns
        df = df.drop(columns=empty_years)

        # Optionally print which years were removed
        if empty_years:
            print(f"Removed years with no data: {empty_years}")

        df["ATC-code"] = atc_codes
        df["Setting"] = setting
        df["Unit"] = unit

        meta_cols = ["ATC-code", "Setting", "Unit"]
        final_cols = meta_cols + [ycol for ycol in year_cols if ycol not in empty_years]

        return df[final_cols]


# Example usage of the MedStatScraperNrUsersSSRI class

if __name__ == "__main__":
    # Specify the URL to scrape
    url = "https://example.com/statistical-data"

    # Create an instance of the scraper
    scraper = MedStatScraperNrUsersSSRI(url)

    try:
        # Fetch the HTML content
        scraper.fetch_html()

        # Parse the statistical data table
        scraper.parse_table()

        # Format the parsed data into a DataFrame
        df = scraper.format_dataframe()

        # Display the resulting DataFrame
        print(df)

    except Exception as e:
        print(f"An error occurred: {e}")
