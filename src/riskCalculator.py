class RiskCalculator:

    def main(self, entry_price, stop_price, risk):
        account_size: int = 100000
        # entry_price: int = 10000 
        # stop_price: int = 9995
        risk_percentage: float = 0.01 
        # hardcoding for now 
        if risk == "low":
            risk_percentage = 0.05
        elif risk == "med":
            risk_percentage = 0.02
        elif risk == "high":
            risk_percentage = 0.01
        elif risk == "extreme":
            risk_percentage = 0.005

        size = (account_size * risk_percentage) / (abs(entry_price - stop_price))
        # print(size)
        return int(size)
