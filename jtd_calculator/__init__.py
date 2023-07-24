""" A.	Jump to Default
I'll make a few assumptions for this model:

1. Bonds with higher coupon rates are assumed to have a higher recovery rate because they provide more
cash flow to the bondholder.

2. Larger issued amounts are assumed to have a lower recovery rate because it's harder to recover a large
amount of money in case of default.

3. The composite rating is assumed to impact the recovery rate. High rated bonds (AAA, AA) have a higher
recovery rate than low rated bonds (B, CCC).

4. Maturity type: Bonds that are callable or putable may have different LGDs compared to bonds without
these features. For simplicity, let's assume that callable bonds have a lower recovery rate as the issuer
has the right to repurchase the bond before maturity.
"""


class JtdCalculator:
    """
    A class used to calculate the Jump to Default (JTD) for a bond.

    Attributes
    ----------
    face_value : float
        The nominal value or principal of the bond.
    coupon_rate : float
        The annual coupon rate of the bond.
    maturity_type : str
        The type of bond based on maturity. For example, 'Callable', 'Putable', etc.
    composite_rating : str
        The credit rating of the bond. For example, 'AAA', 'AA', etc.

    Methods
    -------
    calculate_jtd():
        Calculates the Jump to Default (JTD) of the bond.

    calculate_lgd():
        Calculates the Loss Given Default (LGD) based on the bond's attributes.

    calculate_default_prob():
        Calculates the probability of default based on the bond's composite rating.
    """

    def __init__(self, face_value, coupon_rate, maturity_type, composite_rating):
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.maturity_type = maturity_type
        self.composite_rating = composite_rating
        self.lgd = self.calculate_lgd()
        self.default_prob = self.calculate_default_prob()
        self.jtd = self.calculate_jtd()

    @property
    def face_value(self):
        return self._face_value

    @face_value.setter
    def face_value(self, value):
        self._face_value = value

    @property
    def default_prob(self):
        return self._default_prob

    @default_prob.setter
    def default_prob(self, value):
        self._default_prob = value

    def calculate_jtd(self):
        """
        Calculates the Jump to Default (JTD) of the bond.

        Returns
            float: The JTD, calculated as `lgd * face_value * default_prob`.
        """
        return self.lgd * self.face_value * self.default_prob

    def calculate_lgd(self):
        """
        Calculates and returns the Loss Given Default (LGD) based on the bond's attributes.

        LGD is calculated as `(1 - recovery_rate)*100`, where `recovery_rate` is determined by
        factors such as coupon rate, face value, maturity type, and composite rating.

        Returns
            float: The LGD of the bond.
        """
        recovery_rate = 0.4  # base recovery rate
        if self.coupon_rate > 0.05:
            recovery_rate += 0.1
        if self.face_value > 1e9:  # assuming issued amount is in USD, can adjust depending on data
            recovery_rate -= 0.1
        if self.maturity_type == 'Callable' or self.maturity_type == 'Putable':
            recovery_rate -= 0.1
        if self.composite_rating in ['AAA', 'AA']:
            recovery_rate += 0.1
        elif self.composite_rating in ['B', 'CCC']:
            recovery_rate -= 0.1

        # Ensuring recovery rate stays within bounds
        recovery_rate = min(max(recovery_rate, 0), 1)

        return (1 - recovery_rate)*100

    def calculate_default_prob(self):
        """
        Calculates and returns the probability of default based on the bond's composite rating.

        The default probability varies according to the bond's rating.

        Returns
            float: The default probability of the bond.
        """
        default_prob = 0.00
        if self.composite_rating in ['AAA', 'Aaa']:
            default_prob += 0.00015
        elif self.composite_rating in ['AA', 'Aa']:
            default_prob += 0.001
        elif self.composite_rating in ['A', 'A-']:
            default_prob += 0.002
        elif self.composite_rating in ['BBB', 'Ba']:
            default_prob += 0.02
        elif self.composite_rating in ['B', 'B-']:
            default_prob += 0.05
        else:
            default_prob += 0.1
        return default_prob
