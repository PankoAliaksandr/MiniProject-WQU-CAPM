# Libraries
import pandas as pd
from pandas_datareader import data as pdr
from pandas_datareader._utils import RemoteDataError
import statsmodels.api as sm


# Class which analyze a stock based on historical data
class Analysis:
    # Constructor
    def __init__(self, stock_name, index_name, start_date, end_date,
                 risk_free_rate):
        self.__stock_name = stock_name
        self.__index_name = index_name
        self.__start_date = start_date
        self.__end_date = end_date
        self.__risk_free_rate = risk_free_rate
        self.__stock_data = pd.DataFrame()
        self.__index_data = pd.DataFrame()
        self.__stock_returns = pd.DataFrame()
        self.__index_returns = pd.DataFrame()

        self.__download_hist_data()

    # Download historical data
    def __download_hist_data(self):
        # Download data from Yahoo Finance
        try:
            self.__stock_data = pdr.get_data_yahoo(self.__stock_name,
                                                   start=self.__start_date,
                                                   end=self.__end_date)
        except RemoteDataError:
            # handle error
            print 'Stock symbol "{}" is not valid'.format(self.__stock_name)

        try:
            self.__index_data = pdr.get_data_yahoo(self.__index_name,
                                                   start=self.__start_date,
                                                   end=self.__end_date)
        except RemoteDataError:
            # handle error
            print 'Stock symbol "{}" is not valid'.format(self.__index_name)

        self.__stock_data = self.__stock_data['Adj Close']

        self.__stock_data.dropna(inplace=True)

        self.__index_data = self.__index_data['Adj Close']

        self.__index_data.dropna(inplace=True)

    def get_stock_data(self):
        return self.__stock_data

    def get_index_data(self):
        return self.__index_data

    def get_stock_returns(self):
        return self.__stock_returns

    def get_index_returns(self):
        return self.__index_returns

    def calculate_daily_returns(self):
        self.__stock_returns = self.__stock_data.pct_change(1)
        # Drop first line with NA
        self.__stock_returns.dropna(inplace=True)

        self.__index_returns = self.__index_data.pct_change(1)
        # Drop first line with NA
        self.__index_returns.dropna(inplace=True)

    def implement_regression(self):
        explanatory_variable = sm.add_constant(self.__index_returns)
        model = sm.OLS(self.__stock_returns - self.__risk_free_rate,
                       explanatory_variable - self.__risk_free_rate)
        results = model.fit()
        return results.summary()

    def main(self):
        self.calculate_daily_returns()
        regression_results = self.implement_regression()
        print '\n', regression_results


stock_name = 'ORCL'
index_name = '^GSPC'
start_date = '2015-03-26'
end_date = '2015-06-25'
risk_free_rate = 0.001

analysis = Analysis(stock_name, index_name, start_date, end_date,
                    risk_free_rate)
analysis.main()
