import numpy as np
from pydantic import BaseModel
from typing import Optional, List
import numpy_financial as npf
import QuantLib as ql
import datetime


class Bond(BaseModel):

    """
        This class represents a bond with several characteristics and methods to calculate
        different bond metrics.

        Attributes:
            bond_type (str): The type of bond.
            face_value (float): The face value of the bond.
            coupon_rate (float): The coupon rate of the bond.
            maturity (float): The maturity of the bond in years.
            yield_to_maturity (float, optional): The yield to maturity of the bond.
            npv (float, optional): The net present value of the bond.
            issue_date (datetime.datetime): The issue date of the bond.
            maturity_date (datetime.datetime): The maturity date of the bond.

        Methods:
        calculate_npv_ytm(discount_rate: float) -> Tuple[float, float]:
            Calculates the net present value (NPV) and yield to maturity (YTM) of the bond given a discount rate.

        calculate_spread(risk_free_rate: float, discount_rate: float) -> float:
            Calculates the bond spread which is the difference between the yield of the bond and the risk-free rate.

        calculate_present_value(discount_rate: float) -> float:
            Calculates the present value of the bond given a discount rate.

        calculate_cash_flows(discount_rate: float) -> List[float]:
            Calculates the bond's cash flows at each period, discounted at the given rate.

        calculate_duration(discount_rate: float) -> float:
            Calculates the Macaulay Duration of the bond, which measures the bond's price sensitivity to interest rate
            changes.
    """

    bond_type: str
    face_value: float
    coupon_rate: float
    maturity: float
    yield_to_maturity: Optional[float] = None
    npv: Optional[float] = None
    issue_date: datetime.datetime
    maturity_date: datetime.datetime

    def calculate_npv_ytm(self, discount_rate: float):
        """
        This method calculates the net present value (NPV) and yield to maturity (YTM) of the bond.

        Args:
            discount_rate (float): The rate used for discounting future cash flows.

        Returns:
            Tuple[float, float]: The NPV and YTM of the bond.
        """

        cash_flows = self.calculate_cash_flows(discount_rate)
        npv = npf.npv(discount_rate / 2, cash_flows)  # Discount rate is adjusted for semi-annual periods

        # Calculate IRR (YTM) with QuantLib
        today = ql.Date(self.issue_date.day, self.issue_date.month, self.issue_date.year)
        maturity = ql.Date(self.maturity_date.day, self.maturity_date.month, self.maturity_date.year)
        ql.Settings.instance().evaluationDate = today
        bond_schedule = ql.Schedule(today, maturity, ql.Period(ql.Semiannual),
                                    ql.UnitedStates(ql.UnitedStates.GovernmentBond), ql.Unadjusted, ql.Unadjusted,
                                    ql.DateGeneration.Backward, False)

        bond = ql.FixedRateBond(2, self.face_value, bond_schedule, [self.coupon_rate],
                                ql.ActualActual(ql.ActualActual.Bond))
        day_count = ql.ActualActual(ql.ActualActual.ISMA)
        discount_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, discount_rate, day_count))
        bond.setPricingEngine(ql.DiscountingBondEngine(discount_curve))
        ytm = bond.bondYield(day_count, ql.Compounded, ql.Semiannual)
        self.yield_to_maturity = ytm
        self.npv = npv

        return npv, ytm

    def calculate_spread(self, risk_free_rate: float, discount_rate: float) -> float:
        """
        This method calculates the spread of the bond.

        Args:
            risk_free_rate (float): The risk-free rate.
            discount_rate (float): The discount rate.

        Returns:
            float: The bond spread.
        """

        if self.yield_to_maturity is None:
            self.npv, self.yield_to_maturity = self.calculate_npv_ytm(discount_rate)
        bond_yield = self.yield_to_maturity
        spread = bond_yield - risk_free_rate
        return spread

    def calculate_present_value(self, discount_rate: float) -> float:
        """
        This method calculates the present value of the bond's cash flows.

        Args:
            discount_rate (float): The rate used for discounting future cash flows.

        Returns:
            float: The present value of the bond's cash flows.
        """

        cash_flows = np.full(int(self.maturity * 2) + 1, self.face_value * (self.coupon_rate / 2))
        cash_flows[-1] += self.face_value
        present_value = npf.npv(discount_rate / 2, cash_flows)  # Discount rate is also adjusted for semi-annual periods
        return present_value

    def calculate_cash_flows(self, discount_rate: float) -> List[float]:
        """
        This method calculates the bond's cash flows, discounted at the given rate.

        Args:
            discount_rate (float): The rate used for discounting future cash flows.

        Returns:
            List[float]: A list of the bond's discounted cash flows.
        """
        cash_flows = []
        semi_annual_periods = int(self.maturity * 2)
        coupon_payment = self.face_value * (self.coupon_rate / 2)

        for period in range(1, semi_annual_periods + 1):
            cash_flows.append(coupon_payment)

        cash_flows.append(coupon_payment + self.face_value)

        discounted_cash_flows = []
        for period, cash_flow in enumerate(cash_flows):
            present_value = cash_flow / (1 + discount_rate / 2) ** period
            discounted_cash_flows.append(present_value)

        return discounted_cash_flows

    def calculate_duration(self, discount_rate: float):
        """
        This method calculates the bond duration using QuantLib.

        Args:
            discount_rate (float): The discount rate to calculate bond duration.

        Returns:
            float: The bond duration.
        """

        today = ql.Date(self.issue_date.day, self.issue_date.month, self.issue_date.year)
        maturity = ql.Date(self.maturity_date.day, self.maturity_date.month, self.maturity_date.year)
        ql.Settings.instance().evaluationDate = today
        bond_schedule = ql.Schedule(today, maturity, ql.Period(ql.Semiannual),
                                    ql.UnitedStates(ql.UnitedStates.GovernmentBond), ql.Unadjusted, ql.Unadjusted,
                                    ql.DateGeneration.Backward, False)

        bond = ql.FixedRateBond(2, self.face_value, bond_schedule, [self.coupon_rate],
                                ql.ActualActual(ql.ActualActual.Bond))

        day_count = ql.ActualActual(ql.ActualActual.ISMA)
        discount_curve = ql.YieldTermStructureHandle(ql.FlatForward(today, discount_rate, day_count))
        bond.setPricingEngine(ql.DiscountingBondEngine(discount_curve))

        yield_value = bond.bondYield(discount_rate, day_count, ql.Compounded, ql.Semiannual)
        # yield_value = bond.bondYield(day_count, ql.Compounded, ql.Semiannual)
        interest_rate = ql.InterestRate(yield_value, day_count, ql.Compounded, ql.Semiannual)
        duration = ql.BondFunctions.duration(bond, interest_rate, ql.Duration.Modified)

        return duration*100
