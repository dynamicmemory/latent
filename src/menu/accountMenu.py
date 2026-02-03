from src.menu.menuInterface import IMenu
from src.menu.menuUtilities import *
from src.settings.settings import Settings

class AccountMenu(IMenu):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.options = 6


    def run(self) -> None:
        menu_runner()


account_menu: str = """
1. Account overview 
2. Place limit order 
3. Place market order 
4. Cancel order 
5. Cancel all orders
6. Return to main menu"""

# def manage_account() -> None:
#     """ """
#     options:int = 6 
#     account = AccountManager(api_key=api_key,
#                  api_secret=api_secret, 
#                  testnet=True)
#
#     while True:
#         print_banner("ACCOUNT")
#         dynamic_fprint(account_menu)
#         choice = get_menu_selection(options)
#
#         if choice == 1: 
#             # Refine this into a single call to account
#             account.print_all_balances()
#             account.print_all_usdt_positions()
#             account.print_orders("linear", "BTCUSDT")
#         elif choice == 2:
#             dynamic_fprint(choose_asset_menu)
#             asset = ASSET_MAP[get_menu_selection(1)]
#             dynamic_fprint(choose_side_menu)
#             side = "Buy" if get_menu_selection(2) == 1 else "Sell"
#             size = input("Enter amount: >> ")
#             price = input("Enter price: >> ")
#             account.create_limit_order(asset, side, size, price)
#         elif choice == 3:
#             dynamic_fprint(choose_asset_menu)
#             asset = ASSET_MAP[get_menu_selection(1)]
#             dynamic_fprint(choose_side_menu)
#             side = "Buy" if get_menu_selection(2) == 1 else "Sell"
#             size = input("Enter amount: >> ")
#             account.create_market_order(asset, side, size)
#         elif choice == 4:
#             dynamic_fprint(choose_asset_menu)
#             asset: str = ASSET_MAP[get_menu_selection(1)]
#             orders: list|int = account.print_orders("linear", asset)
#             if isinstance(orders, int) or len(orders) == 0:
#                 continue
#             print("Select the 'No' of the order you want to cancel")
#             order_id: int = get_menu_selection(len(orders))
#             account.cancel_order("linear", asset, orders[order_id-1])
#         elif choice == 5:
#             account.cancel_all_USDT_orders("linear")
#         elif choice == 6:
#             break 
#
#         input("\n>> Hit enter to continue")
