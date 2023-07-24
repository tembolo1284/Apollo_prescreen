# Pricing_API

Pricing_API is a FastAPI-based microservice designed to calculate several important metrics for bond investments. This package is part of a larger project, along with the bond_pricing and credit_yield_curve packages.

## Installation

Use the `setup.py` file in the main directory to install the project and its dependencies.

## Usage

Run the application by using the command: `uvicorn pricing_API.main:app --reload`

This will launch a FastAPI application, by default on `localhost:8000`.

## API Endpoints

### GET `/calculate_bond`

This endpoint calculates the Net Present Value (NPV), Internal Rate of Return (IRR), Yield to Maturity (YTM), and Spread of a bond based on the provided bond inputs.

#### Parameters

- `bond_type`: The type of bond (Corporate, Municipal, etc.)
- `face_value`: The face value of the bond.
- `coupon_rate`: The bond's coupon rate.
- `maturity`: The bond's maturity in years.
- `yield_to_maturity`: The bond's yield to maturity. This is optional.

#### Response

The response is a JSON object containing the following fields:

- `NPV`: The Net Present Value of the bond.
- `IRR`: The Internal Rate of Return of the bond.
- `YTM`: The Yield to Maturity of the bond.
- `Spread`: The Spread of the bond.

#### Example

```json
{
    "bond_type": "Corporate",
    "face_value": 1000.0,
    "coupon_rate": 0.05,
    "maturity": 5.0,
    "yield_to_maturity": 0.06,
}
