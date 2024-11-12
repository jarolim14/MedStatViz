from typing import List, Union, Optional
import json
from urllib.parse import quote


class MedStatURLGenerator:
    """Class for generating MedStat URLs with parameter validation."""

    BASE_URL = "https://medstat.dk/en/viewDataTables/medicineAndMedicalGroups/"
    DEFAULT_YEARS = ["2023", "2022", "2021"]

    VALID_SECTORS = {"0", "1", "2"}
    VALID_GENDERS = {"A", "1", "2"}
    VOLUME_VARIABLES = {
        "sold_volume",
        "sold_volume_1000_day",
    }

    # Reference dictionary for available options
    MEDSTAT_OPTIONS = {
        "region": {
            "0": "Denmark",
            "1": "Capital Region",
            "2": "Region Zealand",
            "3": "Region of Southern Denmark",
            "4": "Central Denmark Region",
            "5": "North Denmark Region",
        },
        "sector": {"0": "Primary Sector", "1": "Hospital Sector", "2": "Total"},
        "gender": {"A": "All", "1": "Men", "2": "Women"},
        "age_group": {
            "A": "All",
            "[15, 16, 17, 18]": "15, 16, 17, 18 year olds",
        },
        "search_variable": {
            "people_count": "Number of users",
            "people_count_1000": "Number of users per 1000 inhabitants",
            "sold_volume": "Sold volume",
            "sold_volume_1000_day": "Sold volume per 1,000 inhabitants per day",
        },
    }

    def __init__(self):
        """Initialize the URL generator."""
        pass

    @staticmethod
    def format_age_codes(ages: List[int]) -> List[str]:
        """Convert list of ages to zero-padded, three-digit string codes."""
        return [f"{age:03}" for age in ages]

    @classmethod
    def print_options(cls, category: Optional[str] = None) -> None:
        """
        Print available options for MedStat parameters.

        Args:
            category: Specific category to print (None for all categories)
        """
        if category and category in cls.MEDSTAT_OPTIONS:
            print(f"\n{category.upper()} OPTIONS:")
            for key, value in cls.MEDSTAT_OPTIONS[category].items():
                print(f"  {key}: {value}")
        else:
            print("\nAVAILABLE OPTIONS:")
            for category, options in cls.MEDSTAT_OPTIONS.items():
                print(f"\n{category.upper()}:")
                for key, value in options.items():
                    print(f"  {key}: {value}")

    def print_all_options(self):
        """Print all available options for MedStat parameters."""
        self.print_options()
        print("")
        print(
            "Note that non-primary sectors only support volume measurements and cannot filter by gender or age group"
        )

        print(
            "If you want to filter by gender or age group, set sector to '0' (Primary Sector)"
        )

    def generate_url(
        self,
        atc_codes: List[str],
        *,  # Force keyword arguments
        years: Optional[List[str]] = None,
        region: str = "0",
        sector: str = "0",
        gender: Union[str, List[str]] = "A",
        age_group: str = "A",
        search_variable: str = "sold_volume",
    ) -> str:
        """
        Generate a MedStat URL based on the given parameters.

        Args:
            atc_codes: List of ATC codes to include
            years: List of years (default: last 3 years)
            region: Region code (default: "0" for Denmark)
            sector: Sector code ("0": Primary, "1": Hospital, "2": Total)
            gender: Gender code ("A": All, "1": Men, "2": Women) or list of codes
            age_group: Age group code (default: "A" for All)
            search_variable: Type of data to search for (default: "sold_volume")

        Returns:
            Formatted MedStat URL
        """
        try:
            # Input validation
            if not isinstance(atc_codes, list):
                raise TypeError("atc_codes must be a list")

            if sector not in self.VALID_SECTORS:
                raise ValueError(f"Invalid sector: {sector}")

            # check if years are beyond 1996 and 2023
            if years:
                for year in years:
                    if int(year) < 1996 or int(year) > 2023:
                        raise ValueError("Year must be between 1996 and 2023")

            # Set defaults and normalize inputs
            years = years or self.DEFAULT_YEARS
            gender_list = [gender] if isinstance(gender, str) else gender

            # Handle age group formatting
            if age_group == "A":
                age_group_codes = ["A"]
            elif isinstance(age_group, list):
                age_group_codes = self.format_age_codes(age_group)
            else:
                raise TypeError("age_group must be 'A' or a list of integers")

            # Validate sector-specific constraints
            if sector != "0":  # If not primary sector
                if (
                    any(g != "A" for g in gender_list)
                    or age_group != "A"
                    or search_variable not in self.VOLUME_VARIABLES
                ):
                    raise ValueError(
                        "Non-primary sectors only support volume measurements "
                        "and cannot filter by gender or age group"
                    )

            # Construct query parameters
            params = {
                "year": years,
                "region": [region],
                "gender": gender_list,
                "ageGroup": age_group_codes,
                "searchVariable": [search_variable],
                "errorMessages": [],
                "atcCode": atc_codes,
                "sector": [sector],
            }

            return f"{self.BASE_URL}{quote(json.dumps(params))}"

        except (ValueError, TypeError) as e:
            print(f"\nError: {str(e)}")
            self.print_options()
            raise


## example ## example## example## example## example## example## example## example
# atc_codes = ["N06A", "N06AA", "N06AB", "N06AF", "N06AG", "N06AX"]
#
# generator = MedStatURLGenerator()
#
# # Example with a single gender
# url_single = generator.generate_url(
#     atc_codes,
#     years=["2023", "2022", "2021"],
#     region="0",
#     sector="0",
#     gender="1",
#     age_group="A",
#     search_variable="sold_volume",
# )  # Men
#
# print("\nSingle Gender URL:", url_single)
#
# # Example with multiple genders
# url_multiple = generator.generate_url(
#     atc_codes,
#     years=["2023", "2022", "2021"],
#     region="0",
#     sector="0",
#     gender=["1", "2"],
#     age_group="A",
#     search_variable="sold_volume",
# )  # Men and Women
# print("\nMultiple Gender URL:", url_multiple)
#
# # This will raise an error and print options
# url_error = generator.generate_url(
#     atc_codes,
#     sector="1",  # Hospital sector
#     gender=["1", "2"],  # Not allowed for hospital sector
# )
