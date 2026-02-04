from src.accountManager import AccountManager
from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class AccountMenu(IMenu):
    def __init__(self, settings: Settings, account: AccountManager):
        self.settings = settings
        self.account = account
        self.menu: dict[int, list] = {
            1: ["Overview", self.overview],
            2: ["Place Limit Buy", self.place_limit_buy],
            3: ["Place Limit Sell", self.place_limit_sell],
            4: ["Market Buy", self.market_buy],
            5: ["Market Sell", self.market_sell],
            6: ["Cancel Order", self.cancel_order],
            7: ["Cancel All Orders", self.cancel_all_orders],
            8: ["Change Asset & Timeframe", self.change_asset_and_timeframe],
         }

 
    def run(self) -> None:
        args: list = [convert_asset_tostring(self.settings.asset()), 
                      convert_timeframe_tostring(self.settings.timeframe())]
        menu_runner(title, self.menu, header, args)


    def overview(self) -> None:
        # Refine this into a single call to account
        self.account.print_all_balances()
        self.account.print_all_usdt_positions()
        self.account.print_orders("linear", "BTCUSDT")
        input("\n>> Hit enter to continue")


    # TODO: Add checks and better instructions on size and price
    def place_limit_buy(self) -> None:
        asset = convert_asset_tostring(self.settings.asset())
        size = input("Enter amount: >> ")
        price = input("Enter price: >> ")
        self.account.create_limit_order(asset, "Buy", size, price)
        input("\n>> Hit enter to continue")


    # TODO: Add checks and better instructions on size and price
    def place_limit_sell(self) -> None:
        asset = convert_asset_tostring(self.settings.asset())
        size = input("Enter amount: >> ")
        price = input("Enter price: >> ")
        self.account.create_limit_order(asset, "Sell", size, price)
        input("\n>> Hit enter to continue")


    # TODO: Add checks and better instructions on size 
    def market_buy(self) -> None:
        asset = convert_asset_tostring(self.settings.asset())
        size = input("Enter amount: >> ")
        self.account.create_market_order(asset, "Buy", size)
        input("\n>> Hit enter to continue")


    # TODO: Add checks and better instructions on size 
    def market_sell(self) -> None:
        asset = convert_asset_tostring(self.settings.asset())
        size = input("Enter amount: >> ")
        self.account.create_market_order(asset, "Sell", size)
        input("\n>> Hit enter to continue")


    # TODO: Remake this, it is sloppy and error prone
    def cancel_order(self) -> None:
        asset = convert_asset_tostring(self.settings.asset())
        orders: list|int = self.account.print_orders("linear", asset)
        if isinstance(orders, int) or len(orders) == 0:
            return 
        print("Select the 'No' of the order you want to cancel")
        order_id: int = get_menu_selection(len(orders))
        self.account.cancel_order("linear", asset, orders[order_id-1])
        input("\n>> Hit enter to continue")


    def cancel_all_orders(self) -> None:
        self.account.cancel_all_USDT_orders("linear")
        input("\n>> Hit enter to continue")


    # TODO: Build this out to change the asset and timeframe and save to settings
    def change_asset_and_timeframe(self) -> None:
        input("\n>> Hit enter to continue")


title: str = "Account Manager"
header: str = "Current Asset {0} | Current Timeframe {1}\n"
