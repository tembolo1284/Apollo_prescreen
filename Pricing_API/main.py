from fastapi import FastAPI, HTTPException
from bond_pricing.bond_pricing.models import Bond
from pydantic import BaseModel
from typing import Optional
import datetime
import random

app = FastAPI()


class BondInput(BaseModel):
    bond_type: str
    face_value: int
    coupon_rate: float
    maturity: float
    yield_to_maturity: Optional[float] = None
    npv: Optional[float] = None
    issue_date: datetime.datetime
    maturity_date: datetime.datetime


@app.post("/calculate_bond")
async def calculate_bond(bond_input: BondInput):
    try:
        bond = Bond(
            bond_type=bond_input.bond_type,
            face_value=bond_input.face_value,
            coupon_rate=bond_input.coupon_rate,
            maturity=bond_input.maturity,
            yield_to_maturity=bond_input.yield_to_maturity,
            issue_date=bond_input.issue_date,
            maturity_date=bond_input.maturity_date
        )

        discount_rate = random.uniform(0.03, 0.06)  # Can pull from external source
        npv, ytm = bond.calculate_npv_ytm(discount_rate)

        risk_free_rate = 0.04  # Can pull from external source
        spread = bond.calculate_spread(risk_free_rate, discount_rate)

        duration = bond.calculate_duration(discount_rate)

        return {
            "NPV": round(npv, 4),
            "YTM": round(ytm, 4),
            "Spread": round(spread, 4),
            "Duration": round(duration, 4)
        }
    except ValueError as e:
        raise HTTPException(status_code=500, detail="Error: Out of range float values are not JSON compliant.")
