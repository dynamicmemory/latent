# TODO: Class is fine for now, risk needs to be dynamic, probably from outside 
#       the class, same with account size, that will be found outside of class.
class RiskCalculator:

    def main(self, account_size, entry_price, stop_price, risk):
        # account_size: float = 1000.00
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

        # print(risk, risk_percentage)
        if abs(entry_price - stop_price) == 0:
            print("Entry_price - stop_price would be 0, avoiding 0 divide error")
            return 0, 0 

        size = (account_size * risk_percentage) / (abs(entry_price - stop_price))
        size = int(size * entry_price)
        # print(size)
        return size, risk_percentage
