import pandas as pd
import QuantLib as ql
import matplotlib.pyplot as plt


class CreditYieldCurve:
    """
    A class used to represent a simple credit yield curve

    Attributes
    ----------
    data_path : str
        a string that represents the path to the csv data file of bond data

    df : DataFrame
        a pandas DataFrame that holds the sorted data by maturity

    yc_df : DataFrame
        a pandas DataFrame that holds the final, interpolated yield curve data

    Methods
    -------
    load_and_sort_data():
        Loads and sorts the data from the file at data_path

    calculate_yield():
        Calculates the yield for each bond in the data

    construct_yc():
        Constructs a yield curve based on the bond yield data

    plot_yields():
        Plots the yields over time

    plot_yc():
        Plots the yield curve
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.yc_df = None
        self.df = None

    def load_and_sort_data(self):
        """
        Loads and sorts the data by maturity from the file at data_path.
        """
        df = pd.read_csv(self.data_path)
        df['Maturity'] = pd.to_datetime(df['Maturity'], format='%m/%d/%Y')
        df = df.sort_values(by='Maturity')
        self.df = df

    def calculate_yield(self):
        """
        Calculates the yield for each bond in the data using the QuantLib library.

        Returns:
            df (DataFrame): The original DataFrame with an added 'Yield' column.
        """
        yield_list = []
        for index, row in self.df.iterrows():
            settlement_date = ql.Settings.instance().evaluationDate
            maturity_date = ql.Date(row['Maturity'].day, int(row['Maturity'].month), row['Maturity'].year)

            schedule = ql.Schedule(settlement_date, maturity_date, ql.Period(ql.Semiannual),
                                   ql.UnitedStates(ql.UnitedStates.GovernmentBond),
                                   ql.Unadjusted, ql.Unadjusted, ql.DateGeneration.Backward, False)
            bond = ql.FixedRateBond(2, 100, schedule, [row['Cpn']/100], ql.Thirty360(ql.Thirty360.USA))
            bond.setPricingEngine(ql.DiscountingBondEngine(ql.YieldTermStructureHandle(ql.FlatForward(
                settlement_date, row['Ask Price']/100, ql.Thirty360(ql.Thirty360.USA)))))
            yield_list.append(bond.bondYield(ql.Thirty360(ql.Thirty360.USA), ql.Compounded, ql.Semiannual))
        self.df['Yield'] = yield_list
        return self.df

    def construct_yc(self):
        """
        Constructs a yield curve based on the bond yield data. The yield curve is interpolated for a specific
        set of tenors.
        """
        at_maturity_df = self.df[self.df['Maturity Type'] == 'AT MATURITY'].copy()
        tenors = ['1m', '3m', '6m', '1y', '2y', '3y', '5y', '7y', '10y', '20y', '30y', '50y', '70y']
        tenors_in_years = [1 / 12, 3 / 12, 6 / 12, 1, 2, 3, 5, 7, 10, 20, 30, 50, 70]
        today = pd.to_datetime(ql.Date.todaysDate().ISO())
        at_maturity_df.loc[:, 'Maturity Years'] = at_maturity_df['Maturity'].apply(lambda x: (x - today).days / 365.25)
        result_list = []
        for tenor, tenor_year in zip(tenors, tenors_in_years):
            lower_bond = at_maturity_df[at_maturity_df['Maturity Years'] <= tenor_year].iloc[-1]
            upper_bond = at_maturity_df[at_maturity_df['Maturity Years'] >= tenor_year].iloc[0]
            if lower_bond['Maturity Years'] == upper_bond['Maturity Years']:
                interpolated_yield = lower_bond['Yield']
            else:
                slope = (upper_bond['Yield'] - lower_bond['Yield']) / (
                        upper_bond['Maturity Years'] - lower_bond['Maturity Years'])
                interpolated_yield = slope * (tenor_year - lower_bond['Maturity Years']) + lower_bond['Yield']
            result_list.append({'Tenor': tenor, 'Yield': interpolated_yield})
        self.yc_df = pd.DataFrame(result_list)

    def plot_yields(self):
        """
        Plots the yields over time using matplotlib. The x-axis is maturity and the y-axis is yield.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['Maturity'], self.df['Yield'], label='Yields')
        plt.xlabel('Maturity')
        plt.ylabel('Yield')
        plt.title('IBM Bond Yields Plot')
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_yc(self):
        """
        Plots the yield curve using matplotlib. The x-axis is the tenor and the y-axis is the yield.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.yc_df['Tenor'], self.yc_df['Yield'], label='Interpolated Yield Curve')
        plt.xlabel('Tenor')
        plt.ylabel('Yield')
        plt.title('Interpolated Yield Curve')
        plt.grid(True)
        plt.legend()
        plt.show()
