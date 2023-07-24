from setuptools import setup, find_packages

setup(
    name='financial_calculations',
    version='1.0',
    packages=find_packages(include=['credit_yield_curve', 'bond_pricing', 'pricing_API', 'bond_pricing.*',
                                    'credit_yield_curve.*', 'pricing_API.*', 'jtd_calculator', 'jtd_calculator.*']),
    install_requires=[
        'pandas',
        'matplotlib',
        'QuantLib',
        'fastapi',
        'uvicorn',
        'pydantic',
        'numpy_financial',
        'numpy',
        'httpx',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'credit_yield_curve=credit_yield_curve.curve:main',
            'pricing_API=pricing_API.main:app',
        ],
    },
    python_requires='>=3.7',
)
