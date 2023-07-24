from credit_yield_curve.construct_curve import CreditYieldCurve


def main():
    data = 'bond_data.csv'  # Replace with the actual path to your data file
    curve = CreditYieldCurve(data)
    curve.load_and_sort_data()
    curve.calculate_yield()
    curve.construct_yc()
    # curve.plot_yields() #  plots all yields available in the bond_data csv
    curve.plot_yc()  # interpolated and smoothed out yield curve based off bond_data


if __name__ == '__main__':
    main()
