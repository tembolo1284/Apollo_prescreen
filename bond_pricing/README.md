# Bond Pricing

Bond Pricing is a Python module designed to calculate various metrics for bonds such as Net Present Value (NPV), Yield to 
Maturity (YTM), spread over risk-free rate, and duration. It uses numpy_financial for financial calculations and QuantLib 
for bond yield and duration calculations.

## Installation

Use the `setup.py` file in the main directory to install the project and its dependencies.

## Usage

The main object in this package is the Bond object. Here's an example of how you might use the Bond class:The primary class 
for bond calculations is the `Bond` class, which takes bond characteristics as inputs. Here's an example usage:

```python
from bond_pricing.models import Bond
import datetime

# Define bond parameters
bond_type = 'Corporate'
face_value = 1000
coupon_rate = 0.05
maturity = 5
issue_date = datetime.datetime(2020, 1, 1)
maturity_date = datetime.datetime(2025, 1, 1)

# Create bond object
bond = Bond(
    bond_type=bond_type,
    face_value=face_value,
    coupon_rate=coupon_rate,
    maturity=maturity,
    issue_date=issue_date,
    maturity_date=maturity_date
)

# Calculate NPV and YTM
discount_rate = 0.04
npv, ytm = bond.calculate_npv_ytm(discount_rate)
print(f"NPV: {npv:.2f}")
print(f"YTM: {ytm:.4%}")

# Calculate Spread
risk_free_rate = 0.03
spread = bond.calculate_spread(risk_free_rate, discount_rate)
print(f"Spread: {spread:.4%}")

# Calculate Duration
duration = bond.calculate_duration(discount_rate)
print(f"Duration: {duration:.4f}")

