"""
Author: Phyo Thiha
Last Modified: September 11, 2019
Description: This is to calculate DMA weights (indexes) for
individual networks (Market_Monthly_Trend), for each market based on
national ratings (Network_Monthly_Trend), both of which we have
downloaded using Selenium.
"""
import pandas as pd


df = pd.read_excel('Network_Monthly_Trend_M_Z_Networks_All_Markets_20190101_20190901.xlsx',
                   index_col=0, skiprows=5, skipfooter=6)

df.loc[df.index[0],'Jan\n\'19']

