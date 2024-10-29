# MedStat Scraper and Plotter

This project is designed to retrieve data from MedStat into Python. It entails a URL generator, a scraper, and a simple plotter.

## Project Structure

- `ExampleUsage.ipynb`: Jupyter Notebook demonstrating how to use the modules in this project.
- `MedStatURLGenerator.py`: This class generates the searh URL for MedStat based on ACT codes, time frames, and more.
- `MedStatScraper.py`: This class scrapes the data from MedStat and returns a clean pandas dataframe.
- `MedStatPlotter.py`: Contains a simple plotting class to plot the data as line plots.

- `N06A_MedStat_ATC_Dictionary.json`: JSON file containing a dictionary for ATC classification, only the N06A class is included for our example.
- `README.md`: This file, providing an overview of the project.

## Usage
1. **Generating URLs**: Use the functions in [`MedStatURLGenerator.py`](MedStatURLGenerator.py) to generate URLs for accessing medical statistics data.
2. **Scraping Data**: Use the functions in [`MedStatScraper.py`](MedStatScraper.py) to scrape data from your desired sources.
3. **Plotting Data**: Use the functions in [`MedStatPlotter.py`](MedStatPlotter.py) to plot the scraped data.

## Example

Refer to the [`ExampleUsage.ipynb`](ExampleUsage.ipynb) notebook for an example of how to use the modules in this project.

## Dependencies

Make sure to install the required dependencies before running the scripts. You can install them using:
pip install -r requirements.txt

## License
This project is licensed under the MIT License.
