import pandas as pd
import yfinance as yf
import os
import glob
from datetime import datetime, timedelta


# Create the necessary directory if it doesn't exist
data_dir = f"{os.getcwd()}/data/stocks"
os.makedirs(data_dir, exist_ok=True)

company_dict = {
    "APPLE": "AAPL",
    "GOOGLE": "GOOG",
    "MICROSOFT": "MSFT",
    "AMAZON": "AMZN",
}


def initialize_dataset(period=5):

    end = datetime.now()
    start = datetime(end.year - period, end.month, end.day)

    for stock in company_dict.keys():
        df = yf.download(company_dict[stock], start, end)
        df.to_csv(f"{data_dir}/{stock}.csv")


def add_to_dataset():
    for file in glob.glob(f"{data_dir}/*.csv"):
        stock = os.path.basename(file).split(".")[0]
        dataset = pd.read_csv(file, index_col=0, parse_dates=True)

        # Get the last date in the existing dataset
        last_date = dataset.index[-1]

        # Calculate the start date for downloading new data
        start = last_date + timedelta(days=1)
        end = datetime.now()

        if start <= end:
            new_data = yf.download(company_dict[stock], start, end)

            # Append new data to the existing dataset
            if not new_data.empty:
                updated_dataset = pd.concat([dataset, new_data])
                updated_dataset.to_csv(file)


def data_ingestion():
    # Check if the data directory is empty
    if not os.listdir(data_dir):
        print("Directory is empty. Initializing dataset.")
        initialize_dataset(period=10)
    else:
        print("Directory is not empty. Adding to dataset.")
        add_to_dataset()


if __name__ == "__main__":
    data_ingestion()
