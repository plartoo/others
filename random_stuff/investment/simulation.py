"""
Script to simulate buying stock (in this case, S&P 500)
incrementally over the years and see how the investment
performs under various scenarios and buying strategies.

The S&P 500 historical data can be obtained via Google
Finance API using Google Sheet formula like below:
=GOOGLEFINANCE(".INX", "price", DATE(1970,1,1), DATE(2021,12,31), "DAILY")

The historical consumer price index (CPI) data can be obtained from:
https://www.usinflationcalculator.com/inflation/consumer-price-index-and-annual-percent-changes-from-1913-to-2008/

This script can be used to simulate other stocks (other
than S&P 500) as long as we have their historical data in
the following schema/columns: 'Date', 'Low', 'High'

Replace daily_stock_price_file variable's value with
the stock value file of your choice to run this simulation
for another stock.

REFS:
BLS inflation calculator: https://www.bls.gov/data/inflation_calculator.htm
Another inflation calculator: https://www.usinflationcalculator.com/

"""

import pdb
import pandas as pd

MONTH_NAME_TO_INT = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, June=6,
                         July=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)


def main():
    daily_stock_price_file = 'S&P500.xlsx'
    monthly_cpi_file = 'Monthly_CPI.xlsx'
    output_file = 'Results.xlsx'

    stock_df = pd.read_excel(daily_stock_price_file)
    # Remove time portion in original 'Date' column to only keep the date values
    stock_df['Date'] = stock_df['Date'].dt.date
    # Create 'Year' and 'Month' from the 'Date' column
    stock_df['Year'], stock_df['Month'] = pd.to_datetime(stock_df['Date']).dt.year, \
                                          pd.to_datetime(stock_df['Date']).dt.month
    # Find mid-price between high and low price for each day
    stock_df['Mid'] = stock_df[['Low', 'High']].mean(axis=1)
    stock_df = stock_df[['Date', 'Year', 'Month', 'Mid']]

    cpi_df = pd.read_excel(monthly_cpi_file)
    # REF: https://pandas.pydata.org/docs/user_guide/reshaping.html#reshaping-by-melt
    cpi_df = cpi_df[cpi_df.columns[:-1]].melt(
        id_vars=['Year'],
        var_name='Month',
        value_name='CPI')
    cpi_df = cpi_df.replace({'Month': MONTH_NAME_TO_INT})

    final_df = pd.merge(stock_df, cpi_df, on=['Year', 'Month'], how='left')
    final_df = final_df[final_df['CPI'].notna()]
    final_df.to_excel(output_file, index=False)

    max_date = final_df['Date'].max()
    pdb.set_trace()
    latest_cpi = final_df[final_df['Date'] == max_date]['CPI']
    print("Program ended.")


if __name__ == '__main__':
    main()
