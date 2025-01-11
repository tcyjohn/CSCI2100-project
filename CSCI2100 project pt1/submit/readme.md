Stock Data Retrieval and Analysis

Requirements
    Python: Ensure you have Python 3.x installed on your system.
    Libraries: This program requires the following libraries:
        pandas
        certifi


Install Required Libraries: Create a requirements.txt file with the following content:
pandas
certifi

Then, install the libraries using:
pip install -r requirements.txt

Run the Program: Execute the script using the following command:
python run.py


Outputs Generated
After running the program, the following outputs will be generated in an output directory:

table1.csv:
    Contains market capitalization data for each ticker.
    Columns:
        ticker: The stock ticker symbol.
        market_cap: The market capitalization value.
        pointer: A numerical index for each entry.

table2.csv:
    Contains historical daily price data for each ticker.
    Columns:
        id: A unique identifier for each ticker's data.
        ticker: The stock ticker symbol.
        data: A nested structure holding historical data, including date, open, low, high, close, adjusted close, and volume.

table1_sorted_a.csv:
    Market capitalization data sorted by ticker symbol.

table1_sorted_b.csv:
    Market capitalization data sorted by market capitalization value.
