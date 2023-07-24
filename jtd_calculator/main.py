from jtd_calculator import JtdCalculator
import pandas as pd


def main():
    #  Load data from CSV
    df = pd.read_csv('bond_data.csv')

    #  Pick a random bond from bond_data.csv
    bond_data = df.sample(n=1).iloc[0]

    #  Create an instance of JtdCalculator using bond characteristics
    face_value = bond_data['Issued Amount']
    coupon_rate = bond_data['Cpn']
    maturity_type = bond_data['Maturity Type']
    composite_rating = bond_data['Composite Rating']

    calculator = JtdCalculator(face_value, coupon_rate, maturity_type, composite_rating)
    print(f"Params of the bond: face = {face_value}, cpn={coupon_rate}, maturity_type = {maturity_type}, "
          f"rating={composite_rating}\n")

    #  Calculate LGD
    lgd = calculator.lgd
    print(f"Loss-Given-Default (LGD): {lgd}%")

    #  Calculate JTD
    jtd = calculator.jtd
    print(f"Jump-to-Default (JTD): ${jtd:,.2f}")

    #  Update default probability
    new_default_prob = calculator.default_prob + 0.1  # immediately pull it down to CCC rating
    calculator.default_prob = new_default_prob
    updated_jtd = calculator.calculate_jtd()
    print(f"Updated JTD with 10% increase in default probability: ${updated_jtd:,.2f}")


if __name__ == '__main__':
    main()
