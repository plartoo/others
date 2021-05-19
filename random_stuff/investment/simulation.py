"""
Script to simulate buying stock (in this case, S&P 500)
incrementally over the years and see how the investment
performs under various scenarios and buying strategies.

The S&P 500 historical data can be obtained via Google
Finance API using Google Sheet formula like below:
=GOOGLEFINANCE(".INX", "price", DATE(1970,1,1), DATE(2021,12,31), "DAILY")
OR
=GOOGLEFINANCE(".INX", "high", DATE(1970,1,1), DATE(2021,12,31), "DAILY")
=GOOGLEFINANCE(".INX", "low", DATE(1970,1,1), DATE(2021,12,31), "DAILY")

The historical consumer price index (CPI) data can be obtained from:
https://www.usinflationcalculator.com/inflation/consumer-price-index-and-annual-percent-changes-from-1913-to-2008/

This script can be used to simulate other stocks (other
than S&P 500) as long as we have their historical data in
the following schema/columns: 'Date', 'Low' and 'High'
('Low' and 'High' to calculate the average price of the day).

Replace daily_stock_price_file variable's value with
the stock value file of your choice to run this simulation
for another stock.

REFS:
BLS inflation calculator: https://www.bls.gov/data/inflation_calculator.htm
Another inflation calculator: https://www.usinflationcalculator.com/
"""

import pdb
import numpy as np
import pandas as pd

MONTH_NAME_TO_INT = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, June=6,
                         July=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)


def main():
    daily_stock_price_file = 'S&P500.xlsx'
    monthly_cpi_file = 'Monthly_CPI.xlsx'
    output_file = 'Results.xlsx'
    # How much money one would save for investment each month
    monthly_deposit = 2000.00

    stock_df = pd.read_excel(daily_stock_price_file)
    # Remove time portion in original 'Date' column to only keep the date values
    stock_df['Date'] = stock_df['Date'].dt.date
    # Create 'Year' and 'Month' from the 'Date' column
    stock_df['Year'] = pd.to_datetime(stock_df['Date']).dt.year
    stock_df['Month'] = pd.to_datetime(stock_df['Date']).dt.month

    # Find mid-price between high and low price for each day
    stock_df['Avg_Price'] = stock_df[['Low', 'High']].mean(axis=1)
    stock_df = stock_df[['Date', 'Year', 'Month', 'Avg_Price']]

    cpi_df = pd.read_excel(monthly_cpi_file)
    # REF: https://pandas.pydata.org/docs/user_guide/reshaping.html#reshaping-by-melt
    cpi_df = cpi_df[cpi_df.columns[:-1]].melt(
        id_vars=['Year'],
        var_name='Month',
        value_name='CPI')
    cpi_df = cpi_df.replace({'Month': MONTH_NAME_TO_INT})

    # Join stock and CPI data into one dataframe
    final_df = pd.merge(stock_df, cpi_df, on=['Year', 'Month'], how='left')
    final_df = final_df[final_df['CPI'].notna()]
    final_df.to_excel(output_file, index=False)

    # Capture the most recently available CPI value
    final_df['Date'] = pd.to_datetime(final_df['Date'])
    min_date = final_df['Date'].min()
    max_date = final_df['Date'].max()
    latest_cpi = final_df[final_df['Date'] == max_date]['CPI'].values[0]

    # Fill the date gaps in 'Date' column and copy
    # their corresponding values in other columns
    # (such as 'CPI' and 'Avg_Price') using 'ffill' and 'bfill'
    # REF: https://stackoverflow.com/a/67575184/1330974
    date_range = pd.date_range(
        min_date - pd.tseries.offsets.MonthBegin(),
        max_date,  # + pd.tseries.offsets.MonthEnd()
        name='Date'
    )
    final_df = final_df.set_index('Date').reindex(date_range).reset_index()

    # REF: https://stackoverflow.com/a/67576453/1330974
    final_df['Year'] = final_df.groupby(pd.Grouper(key='Date', freq='1M'))['Year'].ffill().bfill()
    final_df['Month'] = final_df.groupby(pd.Grouper(key='Date', freq='1M'))['Month'].ffill().bfill()
    final_df['Avg_Price'] = final_df.groupby(pd.Grouper(key='Date', freq='1M'))['Avg_Price'].ffill().bfill()
    final_df['CPI'] = final_df.groupby(pd.Grouper(key='Date', freq='1M'))['CPI'].ffill().bfill()

    # Deposit monthly_deposit amount at the beginning of each month
    # REF: https://stackoverflow.com/a/45069536
    final_df = final_df.set_index('Date')
    start_date_of_each_month = final_df.index.to_series().groupby(pd.Grouper(freq='M')).min()
    final_df.loc[start_date_of_each_month, 'Deposit'] = monthly_deposit
    final_df['Deposit'] = final_df['Deposit'].fillna(0.0)
    final_df['Deposit'] = (final_df['Deposit'] * final_df['CPI'])/latest_cpi

    # Create 'Day' column so that we can use it as a reference for calculations later
    final_df = final_df.reset_index()
    final_df['Day'] = pd.to_datetime(final_df['Date']).dt.day
    final_df['Day_of_Week'] = pd.to_datetime(final_df['Date']).dt.day_name()

    # Calculate stock price based (adjusted) on most recent dollar value
    # In other words, adjust the historical stock price based on the current
    # dollar's purchasing power.
    final_df['Constant_Avg_Price'] = (final_df['Avg_Price'] * latest_cpi)/ final_df['CPI']
    final_df = final_df[['Date', 'Year', 'Month', 'Day', 'Day_of_Week',
                         'CPI', 'Avg_Price', 'Constant_Avg_Price', 'Deposit']]

    final_df['Running_Deposit'] = final_df['Deposit'].cumsum()
    final_df[['Withdrawal', 'Running_Withdrawal']] = 0
    final_df.loc[final_df['Day'] == 1, 'Shares_Bought'] = ((final_df['Running_Deposit']
                                                            - final_df['Running_Withdrawal'].cumsum()) /
                                                           final_df['Avg_Price']).apply(np.floor)
    final_df.loc[final_df['Day'] == 1, 'Withdrawal'] = final_df['Shares_Bought'] * final_df['Avg_Price']
    final_df['Running_Withdrawal'] = final_df['Withdrawal'].cumsum()
    final_df.to_excel('Temp.xlsx')
    # pdb.set_trace()
    # TODO: find x-week high and all-time high (ATH)

    # REF: https://stackoverflow.com/a/45469266
    print("Program ended.")


if __name__ == '__main__':
    main()
