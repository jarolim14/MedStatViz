import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class MedStatPlotter:
    """
    A class to plot data from a pandas DataFrame.

    Attributes:
        df (pd.DataFrame): The DataFrame containing the data to plot.
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initializes the MedStatPlotter with a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the data to plot.
        """
        self.df = df

    def plot(self) -> None:
        """
        Plots the data from the DataFrame, displaying trends over years.
        """
        # Get year columns
        year_cols = [col for col in self.df.columns if col.isdigit()]

        # Create figure and axis objects with specified size
        fig, ax = plt.subplots(figsize=(12, 6))

        # Set font properties
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams["font.size"] = 11

        # Define a color palette
        colors = plt.cm.Set2(np.linspace(0, 1, len(self.df)))

        # Plot each line
        for idx, row in self.df.iterrows():
            ax.plot(
                year_cols,
                row[year_cols],
                marker="o",
                label=row["ATC-code"],
                color=colors[idx],
                linewidth=2,
                markersize=6,
            )

        # Customize the plot
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel(
            f"{'DDD' if self.df['Unit'].iloc[0] == 'DDD' else 'Sales'}", fontsize=12
        )
        ax.set_title(
            f"{self.df['Setting'].iloc[0]}: {'DDD' if self.df['Unit'].iloc[0] == 'DDD' else 'Sales'} by ATC Code",
            fontsize=14,
            pad=20,
        )

        # Customize grid
        ax.grid(True, linestyle="--", alpha=0.7)

        # Customize ticks
        ax.tick_params(axis="both", which="major", labelsize=10)
        plt.xticks(rotation=45)

        # Add legend with custom positioning
        ax.legend(
            bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0, frameon=True
        )

        # Adjust layout
        plt.tight_layout()

    def save_plot(self, filename: str, dpi: int = 300) -> None:
        """
        Saves the plot to a file with high resolution.

        Args:
            filename (str): The filename to save the plot.
            dpi (int, optional): The resolution of the saved plot. Default is 300.
        """
        plt.savefig(
            filename, dpi=dpi, bbox_inches="tight", facecolor="white", edgecolor="none"
        )

    def show_plot(self) -> None:
        """Displays the plot."""
        plt.show()


# Example usage
if __name__ == "__main__":
    # Create an instance of MedStatPlotter
    plotter = MedStatPlotter(df)

    # Plot the data
    plotter.plot()

    # Save the plot
    plotter.save_plot("output_plot.png")

    # Show the plot
    plotter.show_plot()
