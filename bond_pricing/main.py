import pandas as pd
from bond_pricing.models import Bond
import random


def main():
    # Load data from CSV
    df = pd.read_csv('bond_data.csv')

    # Pick a random bond from bond_data.csv
    bond_data = df.sample(n=1).iloc[0]
    print(bond_data)
    bond_type = 'Corporate'
    face_value = 100 * bond_data.get('Ask Price')
    coupon_rate = bond_data.get('Cpn') / 100
    yield_to_maturity = bond_data.get('yield_to_maturity') or None

    issue_date = pd.to_datetime(bond_data.get('Issue Date'))
    maturity_date = pd.to_datetime(bond_data.get('Maturity'))
    time_to_maturity = maturity_date - issue_date
    maturity = round(time_to_maturity.days / 365.25)

    print(f"Params of the bond: face = {face_value}, cpn={coupon_rate}, maturity = {maturity}\n")

    bond = Bond(
        bond_type=bond_type,
        face_value=face_value,
        coupon_rate=coupon_rate,
        maturity=maturity,
        yield_to_maturity=yield_to_maturity,
        issue_date=issue_date,
        maturity_date=maturity_date
    )

    discount_rate = random.uniform(0.03, 0.06)  # Can pull from external source
    npv, ytm = bond.calculate_npv_ytm(discount_rate)
    print(f"NPV: {npv:.2f}")
    print(f"YTM: {ytm:.4%}")

    risk_free_rate = 0.04  # Can pull from external source
    spread = bond.calculate_spread(risk_free_rate, discount_rate)
    print(f"Spread: {spread:.4%}")

    duration = bond.calculate_duration(discount_rate)
    print(f"Duration: {duration:.4f}")


if __name__ == '__main__':
    main()
