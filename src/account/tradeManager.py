# Stateful, knows all the details of the current trade, the details for the 
# flip to the other side, the details of risk and any other market related info
from os import wait
from src.account.accountManager import AccountManager 
from src.exchange.apiManager import api_key, api_secret
from enum import Enum 

CATEGORY:str = "linear"

# Decision is the choice the model made
class Decision(Enum):
    SHORT = 0
    LONG  = 1
    HOLD  = 2
    

class TradeManager:
    def __init__(self, account: AccountManager, asset:str, timeframe:str):
        self.account = account
        self.asset: str = asset 
        self.timeframe: str = timeframe
        self.position: int = -1
        self.pos_size: str = "" # Current position size for open position only
        self.risk: str = ""


    def manage_trade(self, decision:float, risk:str):
        """ 
        Runs the flow for a decision, executes a trade, or returns doing 
        nothing at all depending on what the model decided.
        """
        # Do nothing if the model predicted so
        if decision == Decision.HOLD:
            return 
    
        self._get_position()
        self.risk = risk
        # api error from exchange
        if self.position < 0:
            return 
        # Do nothing if we are already doing what the model says to do
        elif decision == self.position:
            msg = "Long" if decision == 1 else "Short" if decision == 0 else "No position"
            print(f"Modelled predicted: {msg}, Already {msg}")
            return

        # Not in any position 
        elif self.position == Decision.HOLD:
            self._open_position(decision)
            return

        # Flip sides of the market
        self._close_position(decision)
        self._open_position(decision)


    # TODO: Add fail safes to ensure operations (deal with in exchange class)
    def cancel_orders_close_position(self):
        """ Automatically closes position and cancels orders. """
        # print("MAKES IT IN")
        self._get_position()
        # print(self.pos_size, self.position)
        if self.position < 0:
            print("Failed to retrive current position, manual close is needed")
            return 
        # No position
        elif self.position == 2:
            return 

        if self.account.cancel_all_USDT_orders("linear") < 0:
            print("Failed to cancel all orders, manual close is needed")
            return 

        side = "Buy" if self.position == 0 else "Sell"

        # print(self.asset, side, self.pos_size)
        self.account.create_market_order(self.asset, side, str(self.pos_size))


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
        self.pos_size = size


    # TODO: Replace with ml values
    def _calc_stop(self, decision, ohlc) -> float:
        """ Calculates the stop loss price for the order"""
        return int(float(ohlc[3])) if decision == 1 else int(float(ohlc[2]))


    def _calc_entry(self, ohlc) -> float:
        """Calculates the entry price for the order """
        return int(float(ohlc[1]))


    # TODO: Replace with ml values or risk profiled values
    def _calc_target(self, decision, entry, stop):
        """Calculate target price for the take profit order"""
        # print(entry, stop)
        if decision == 1:
            return (entry - stop) * 2 + entry
        elif decision == 0: 
            return entry - (stop - entry) * 2


    def _calc_size(self, entry, stop):
        """ 
        Calculates positions size for the next trade.
        """
        account_size = self.account.get_balance(asset="USDT")
        if account_size < 0:
            return 

        risk_percentage: float = 0.01 
        max_size: float = account_size / entry * 3 # *5 is capping pos size 5x lev

        match self.risk:
            case "low":     risk_percentage = 0.03
            case "med":     risk_percentage = 0.02
            case "high":    risk_percentage = 0.01
            case "extreme": risk_percentage = 0.005

        denominator = max(abs(entry - stop), 50)
        if abs(entry - stop) == 0:
            print("Market volatility too high, unable to calculate size")
            # print("Entry -",entry, "Stop -",stop)
            return 0 

        size: float = (account_size * risk_percentage) / denominator#(abs(entry - stop))
        return min(size, max_size) # Cap max size atm


    # TODO: Safeguards for atomic order placing i.e cancel all & close all on single failure.
    def _open_position(self, decision:float):
        """
        Opens a position, stop loss and target order. Cancels all previous 
        orders prior to executing the trade.
        """
        current_candle, one_candle_back = self.account.get_last_two_ohlc(self.asset, self.timeframe)
        if current_candle == -1:
            return 

        side = "Buy" if decision == 1 else "Sell" 
        entry = self._calc_entry(current_candle)
        stop = self._calc_stop(decision, one_candle_back)
        size = self._calc_size(entry, stop)
        target = self._calc_target(decision, entry, stop)

        if size == 0:
            return 

        if self.account.cancel_all_USDT_orders("linear") < 0:
            print("Call to cancel all orders failed")
            return 

        if target is None:
            print("Target set to None, cancelling trades")
            return

        # The position 
        if self.account.create_market_order(self.asset, side, str(size)) == -1:
            return 
         
        # The stop; deicions + 1 will equal 1 when shorting and 2 when longing.
        if self.account.create_stop_loss(self.asset, side, str(size), str(stop), int(decision+1)) == -1:
            self._close_position(decision)
            return 

        # The target 
        side = "Buy" if side == "Sell" else "Buy"
        if self.account.create_limit_order(self.asset, side, str(size), str(target)) == -1:
            self.account.cancel_all_USDT_orders("linear")
            return 


    def _close_position(self, decision:float):
        """Closes the current open position """
        side = "Buy" if decision == 1 else "Sell" 
        # print(self.asset, side, self.pos_size)
        self.account.create_market_order(self.asset, side, self.pos_size)


    def _convert_decision(self, decision:float) -> str:
        """
        Converts an int representation of a models decision into exchange 
        understood values. 0 == "Sell", 1 == "Buy"
        """
        return "Buy" if decision == 1 else "Sell"


    def _calc_risk_reigme(self ):
        pass

