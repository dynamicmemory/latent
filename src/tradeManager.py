# Stateful, knows all the details of the current trade, the details for the 
# flip to the other side, the details of risk and any other market related info
from src.accountManager import AccountManager 
from src.apiManager import api_key, api_secret
from enum import Enum 

CATEGORY:str = "linear"

# Decision is the choice the model made
class Decision(Enum):
    SHORT = 0
    LONG  = 1
    HOLD  = 2
    

class TradeManager:
    def __init__(self, asset:str, timeframe:str):
        self.account = AccountManager(api_key, api_secret)
        self.asset: str = asset 
        self.timeframe: str = timeframe
        self.position: int = -1
        self.size: str = ""


    def manage_trade(self, decision:int):
        # Do nothing if the model predicted so
        if decision == Decision.HOLD:
            return 

        self._get_position()
        if self.position < 0:
            return 
        # Do nothing if we are already doing what the model says to do
        elif decision == self.position:
            print(f"Already {decision}")
            return
        # Not in any position 
        elif self.position == Decision.HOLD:
            self._open_position()
            return

        # Flip sides of the market
        self._close_position()
        self._open_position()
        return 


    def _get_position(self):
        """ 
        Queries the AccountManager for the current accounts position, sets 
        self.position and self.size to returned values on success otherwise -1 
        """
        pos, size = self.account.get_position(CATEGORY, self.asset)
        # Exchange failure
        if pos < 0:
            self.position = -1

        self.position = pos 
        self.size = size

    def _calc_risk_reigme(self ):
        # s = Strategy()
        pass

    def _calc_stop(self):
        pass

    def _calc_entry(self):
        pass 

    def _calc_target(self):
        pass

    def _close_position(self):
        pass 

    def _open_position(self):
        pass

###############################################################################

    #     decision:int = self.torchnn.predict()
    #     decision = 0
    #
    #     # Find current market risk level
    #     self.strategy = Strategy(X)
    #     curr_mkt_risk: str = self.strategy.main()
    #
    #     account = AccountManager(api_key, api_secret, True)
    #     ctrade, csize = account.get_position("linear", self.asset)
    #     if ctrade == -1:
    #         print("Call to get position failed")
    #         return 
    #     # No trade predicted
    #     if decision == 2:
    #         return
    #         print("There is currently no trade to make.")
    #     # Predicted trade matches current position
    #     elif decision == ctrade:
    #         print("Current trade matches current position")
    #         return 
    #     elif decision != ctrade:
    #         # close current trade, calculate & open new trade
    #         self.trade_manager(account, ctrade, csize ,decision, curr_mkt_risk) 
    #         # print("Trade manager loop")
    #         return
    #     else:
    #         print("Unknown error for now")
    #         return
    #
    #
    # def trade_manager(self, account, current_trade:int, current_size:float, pred:int, risk):
    #     print("Start of trade_manager")
    #
    #     # Cancel all stops and limit orders
    #     if account.cancel_all_USDT_orders("linear") < 0:
    #         print("Call to cancel all orders failed")
    #         return 
    #     print("Call to cancel worked")
    #
    #     balance = account.get_balance(asset="USDT")
    #     if balance < 0:
    #         print("Call for balance failed")
    #         return 
    #     print("Call for balance worked")
    #
    #     exchange = Exchange(self.asset, self.timeframe)
    #     ohlc = exchange.get_ohlc()
    #
    #     # Calculate entry, stop, target and size
    #     entry: float = int(float(ohlc[-1][1]))
    #
    #     # Hard coded arbitrary stop for the time being 
    #     stop, target = 0, 0
    #     if pred == 1:
    #         stop: int = int(float(ohlc[-2][3]))
    #         target: int = (entry - stop) * 2 + entry
    #     elif pred == 0: 
    #         stop: int = int(float(ohlc[-2][2]))
    #         target: int = entry - (stop - entry) * 2
    #
    #
    #     print(f"Entry {entry}, Stop {stop}, Target {target}, Account {balance}") 
    #     rc = RiskCalculator()
    #     if balance <= 0 or entry <= 0 or stop <= 0:
    #         print("Error occured in calculating trade details", balance, entry, stop)
    #         return 
    #     size, risk_percentage = rc.main(balance, entry, stop, risk)
    #
    #     print(asset)
    #     print(f"Time Frame:\t{timeframe}")
    #     print(f"Risk Level:\t{risk}")
    #     print(f"Direction:\t{pred}")
    #     print(f"Entry Level:\t${entry}")
    #     print(f"Stop Level:\t${stop}")
    #     print(f"Target pri:\t${target}")
    #     print(f"Size of Pos:\t${size}")
    #
    #
    #     pred_dir = "Buy" if pred == 1 else "Sell"
    #     target_dir = "Sell" if pred_dir == "Buy" else "Buy"
    #     trigger_dir = 1 if pred == "Sell" else 2
    #     size = str(size)
    #     target = str(target)
    #
    #     if current_trade == 2:
    #         print("Not in trade, marketing in")
    #         # Place new order 
    #         # also have to drop stop and target orders
    #         return 
    #     else:
    #         # close current trade 
    #         print("Closing current trade")
    #         account.create_market_order(self.asset, pred_dir, str(current_size))            
    #
    #
    #
    #
