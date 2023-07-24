# JtdCalculator Class

The `JtdCalculator` class is designed to help calculate the Jump to Default (JTD) for a particular bond, given its face value, coupon rate, maturity type, and composite rating. 

## Attributes

- `face_value`: The nominal value or principal of the bond.
- `coupon_rate`: The annual coupon rate of the bond.
- `maturity_type`: The type of bond based on maturity. For example, 'Callable', 'Putable', etc.
- `composite_rating`: The credit rating of the bond. For example, 'AAA', 'AA', etc.
- `lgd`: Loss Given Default, calculated based on the bond's attributes.
- `default_prob`: The probability of default, calculated based on the bond's composite rating.
- `jtd`: Jump to Default, calculated as the product of `lgd`, `face_value` and `default_prob`.

## Methods

### `calculate_jtd(self)`

Returns the Jump to Default (JTD) of the bond, calculated as `lgd * face_value * default_prob`.

### `calculate_lgd(self)`

Calculates and returns the Loss Given Default (LGD) based on the bond's attributes. LGD is calculated as `(1 - recovery_rate)*100`, where `recovery_rate` is determined by factors such as coupon rate, face value, maturity type, and composite rating.

### `calculate_default_prob(self)`

Calculates and returns the probability of default based on the bond's composite rating. The default probability varies according to the bond's rating.

## Properties

The `JtdCalculator` class includes the following properties:

### `face_value`

This property allows you to get and set the face value of the bond.

### `default_prob`

This property allows you to get and set the default probability of the bond.

## Example

```python
from credit_risk import JtdCalculator

# Initialize the JtdCalculator class
jtd_calculator = JtdCalculator(1000000, 0.05, 'Callable', 'A')

# Calculate JTD
print(jtd_calculator.calculate_jtd())
