import pandas as pd
import numpy as np


class Portfolio:

    def __init__(self, cash):
        self.cash = cash
        self.securities = pd.DataFrame(columns=['Tickers', 'Amounts', 'Costs', 'Last Prices'])
        self.past_navs = [cash]
        self.past_securities = [self.securities]

    def nav(self):
        sec_nav = 0
        for i in range(len(self.securities)):
            sec_nav = sec_nav + self.securities['Last Prices'][i] * self.securities['Amounts'][i]
        nn = self.cash + sec_nav
        return nn

    def buy(self, ticker, amount, price):
        self.cash = self.cash - amount * price
        # if the security is already in the portfolio:
        if ticker in self.securities['Tickers'].values:
            old_amount = self.securities.loc[self.securities['Tickers'] == ticker, 'Amounts'].values[0]
            self.securities.loc[self.securities['Tickers'].values == ticker, 'Amounts'] += amount
            if self.securities.loc[self.securities['Tickers'].values == ticker, 'Amounts'].values[0] != 0:
                # if not covering a short position fully
                new_total_cost = old_amount * \
                                 self.securities.loc[self.securities['Tickers'] == ticker, 'Costs'].values[0] + \
                                 amount * price
                new_cost = new_total_cost / (old_amount + amount)
            else:
                # if covering a short position, just copy the previous cost
                new_cost = self.securities.loc[self.securities['Tickers'] == ticker, 'Costs'].values[0]
            self.securities.loc[self.securities['Tickers'] == ticker, 'Costs'] = new_cost
            self.securities.loc[self.securities['Tickers'] == ticker, 'Last Prices'] = price
        else:
            self.securities = self.securities.\
                append({'Tickers': ticker, 'Amounts': amount, 'Costs': price, 'Last Prices': price}, ignore_index=True)

    def sell(self, ticker, amount, price):
        self.cash = self.cash + amount * price
        # if the security is already in the portfolio:
        if ticker in self.securities['Tickers'].values:
            self.securities.loc[self.securities['Tickers'] == ticker, 'Amounts'] -= amount
            self.securities.loc[self.securities['Tickers'] == ticker, 'Last Prices'] = price
        else:  # implies short sell in a new security
            self.securities = self.securities.append({'Tickers': ticker, 'Amounts': -1 * amount,
                                                      'Costs': price, 'Last Prices': price}, ignore_index=True)

    def update_prices(self, df_newprices):  # organised as Tickers and Last Prices
        self.past_navs.append(self.nav())
        self.past_securities.append(self.securities)
        for i in range(len(df_newprices)):
            if df_newprices['Tickers'][i] in self.securities['Tickers'].values:
                self.securities.loc[self.securities['Tickers'] == df_newprices['Tickers'][i], 'Last Prices'] \
                    = df_newprices['Last Prices'][i]

    def return_past_navs(self):
        self.past_navs.append(self.nav())
        return self.past_navs
