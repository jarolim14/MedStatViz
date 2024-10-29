# MedStatScraper

**MedStatScraper** is a Python package designed for scraping and processing drug-related statistical data from the MedStat website. It provides two main classes: `MedStatScraperVolumeSoldADs` and `MedStatScraperNrUsersSSRI`, which allow users to retrieve and manipulate data regarding the volume of drugs sold and the number of users for specific drug classifications.

## Features

- Scrape statistical data from the MedStat website.
- Parse and format data into Pandas DataFrames for easy analysis.
- Handle missing values and data conversion.
- Extract relevant drug information and organize it efficiently.

## Installation

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4 pandas
```

## Usage

### MedStatScraperVolumeSoldADs

This class is used to scrape and process data related to the volume of drugs sold over time.

```python
from MedStatScraper import MedStatScraperVolumeSoldADs

url = "https://medstat.dk/en/viewDataTables/medicineAndMedicalGroups/{...}"  # Provide the correct URL
scraper = MedStatScraperVolumeSoldADs(url)

tr_texts = scraper.scrape_data()
scraper.create_dataframe(tr_texts)
df = scraper.get_dataframe()
print(df)
```

### MedStatScraperNrUsersSSRI

This class is used to scrape and process data regarding the number of users for specific SSRIs (Selective Serotonin Reuptake Inhibitors).

```python
from MedStatScraper import MedStatScraperNrUsersSSRI

url = "https://medstat.dk/en/viewDataTables/medicineAndMedicalGroups/{...}"  # Provide the correct URL
scraper = MedStatScraperNrUsersSSRI(url)

scraper.fetch_html()
scraper.parse_table()
scraper.format_dataframe()
df = scraper.get_dataframe()
print(df)
```

## Methods

### `MedStatScraperVolumeSoldADs`

- `__init__(self, url)`: Initializes the scraper with the provided URL.
- `scrape_data(self)`: Scrapes the data from the specified URL and returns the content of the statistical data table.
- `create_dataframe(self, tr_texts)`: Takes the scraped text data and formats it into a Pandas DataFrame.
- `get_dataframe(self)`: Returns the formatted DataFrame.

### `MedStatScraperNrUsersSSRI`

- `__init__(self, url)`: Initializes the scraper with the provided URL.
- `fetch_html(self)`: Fetches the HTML content from the URL.
- `parse_table(self)`: Parses the HTML to extract table data.
- `format_dataframe(self)`: Formats the extracted table data into a Pandas DataFrame.
- `get_dataframe(self)`: Returns the formatted DataFrame.

## Example

You can use the classes to extract and analyze drug statistics easily. Here’s a brief example of how to use the `MedStatScraperVolumeSoldADs`:

```python
url = "https://medstat.dk/en/viewDataTables/medicineAndMedicalGroups/{...}"  # Replace with a valid URL
scraper = MedStatScraperVolumeSoldADs(url)

tr_texts = scraper.scrape_data()
scraper.create_dataframe(tr_texts)
df = scraper.get_dataframe()
print(df)
```

## License

This project is licensed under the MIT License.

## Contributions

Contributions are welcome! Feel free to submit issues or pull requests to enhance the functionality of the package.

## Contact

For any inquiries or feedback, please contact [Your Name](mailto:your.email@example.com).