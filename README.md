# Financial Calculation Packages

This repository contains several Python packages for performing various financial calculations. Each package focuses on a specific aspect of financial analysis and provides functionalities to compute specific metrics and models. The packages included in this repository are:

1. **bond_pricing**: A package for bond pricing and valuation calculations.
2. **credit_yield_curve**: A package for constructing and analyzing credit yield curves.
3. **jtd_calculator**: A package for computing Jump-to-Default (JTD) risk for bonds.
4. **Pricing_API**: An API package for exposing financial calculation endpoints.

## Package Descriptions

### bond_pricing

The `bond_pricing` package provides tools for pricing and valuing bonds. It includes functionalities for calculating metrics such as Net Present Value (NPV), Internal Rate of Return (IRR), Yield to Maturity (YTM), and spread. The package supports different types of bonds, such as corporate bonds, government bonds, and municipal bonds. It also offers methods for bond cash flow analysis and risk assessment.

### credit_yield_curve

The `credit_yield_curve` package focuses on constructing and analyzing credit yield curves. It provides tools for collecting credit data, interpolating yield curve points, and performing credit risk analysis. The package supports different methodologies for constructing yield curves, including bootstrapping and curve fitting techniques. It also offers functions for assessing credit spreads and generating credit rating curves.

### jtd_calculator

The `jtd_calculator` package specializes in computing Jump-to-Default (JTD) risk for bonds. It takes into account variables such as Loss-Given-Default (LGD), face value of the bond, and default probabilities. The package provides a JtdCalculator class that encapsulates the necessary calculations and allows for easy computation of JTD risk. It offers methods to set default probabilities and calculate JTD values based on user-provided inputs.

### Pricing_API

The `Pricing_API` package is an API package that exposes financial calculation endpoints. It utilizes the functionalities provided by the 
`bond_pricing` package to perform calculations on incoming requests. The API endpoint allows users to calculate bond prices only at the moment. 
Other packages and functionality are under development. The package utilizes the FastAPI framework to handle HTTP requests and responses.

## Getting Started

To use any of the packages included in this repository simply source the virtual environment 
(source venv/Scripts/activate) at the root directory and then type pip install -e .
to install everything from the setup.py file.

Please don't forget to include the period (.) after pip install -e

Please run the below to start the API to begin pricing bonds.


```
uvicorn Pricing_API.main:app --reload

# One can also run the main.py file in any package

python bond_pricing/main.py
python credit_yield_curve/main.py
python jtd_calculator/main.py

# One can also run the test_api.py file in Pricing_API to call the API

python Pricing_API/test_api.py

# One can also test the API by running a curl command such as the below:

curl -X POST http://127.0.0.1:8000/calculate_bond \
-H 'Content-Type: application/json' \
-d '{
    "bond_type": "Corporate",
    "face_value": 1000.0,
    "coupon_rate": 0.05,
    "maturity": 10.0,
    "yield_to_maturity": null,
    "issue_date": "2022-07-20T22:43:59.567602",
    "maturity_date": "2032-07-17T22:43:59.567602"
}'
