# Credit Yield Curve

This package is designed to help with the construction and visualization of credit yield curves. It's built on top of Python's 
powerful libraries such as pandas, QuantLib, and matplotlib.

## Installation

Use the `setup.py` file in the main directory to install the project and its dependencies.

## Usage

To use the Credit Yield Curve module, you need to provide a CSV file with bond data. The CSV file should include at least the following columns:

- `Maturity`: The bond's maturity date.
- `Cpn`: The bond's coupon rate.
- `Ask Price`: The bond's ask price.
- `Maturity Type`: The bond's maturity type.

The main functionality of the Credit Yield Curve module is provided by the `CreditYieldCurve` class. Here's an example usage:

```python
from credit_yield_curve import CreditYieldCurve

# Initialize the CreditYieldCurve class
credit_yield_curve = CreditYieldCurve("path_to_your_data.csv")

# Load and sort the data
credit_yield_curve.load_and_sort_data()

# Calculate the yields for each bond
credit_yield_curve.calculate_yield()

# Construct the yield curve
credit_yield_curve.construct_yc()

# Plot the yields
credit_yield_curve.plot_yields()

# Plot the yield curve
credit_yield_curve.plot_yc()

