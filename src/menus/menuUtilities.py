import pyfiglet

def menu_runner(title: str, options: dict[int, list], header: str, args_callable) -> None:
    menu_length: int =  len(options) + 1 
    while True:
        print_banner(title)
        args = args_callable()
        dynamic_fprint(header, *args)

        for key, (label, _) in options.items():
            print(f"{key}. {label}")
        print(f"{menu_length}. Exit")

        choice = get_menu_selection(menu_length)

        if choice == menu_length:
            return

        _, func = options[choice]

        func()


def print_banner(banner_text:str="Algorithmic Trading SYS") -> None:
    """
    Clears the terminal display and prints a banner for the current menu
           
    Args:
        banner_text: The text to print inside the banner, default to app name.
    """
    print("\033c", end="")
    text = pyfiglet.figlet_format(banner_text, font="slant")
    print(text)
    print("-"*70)


def dynamic_fprint(template:str, *args:list):
    if template == "":
        return
    print(template.format(*args))

    
def get_menu_selection(options:int) -> int:
    """ Returns the selected menu item """
    print("-"*70)
    while True:
        try:
            choice = int(input("\n>> "))
        except (ValueError, TypeError):
            print("Enter a number from the provided options")
            continue

        if choice > 0 and choice < options+1:
            return choice 
        print("Enter a number from the provided options")


# MAP RELATED UTILS
def asset_tostring(record: int) -> str:
    """Returns the record from the asset map that matches the integer passed in"""
    return ASSET_MAP[record]


def timeframe_tostring(record: int) -> str:
    """Returns the record from the time map that matches the integer passed in"""
    return TIME_MAP[record]


def choose_timeframe() -> str:
    for k, v in TIME_MAP.items():
        if k == 0:
            continue
        print(f"{k}. {v}")
    choice = get_menu_selection(len(TIME_MAP)-1) # -1 for 0 option
    return TIME_MAP[choice]


def choose_asset() -> str: 
    for k, v in ASSET_MAP.items():
        if k == 0:
            continue 
        print(f"{k}. {v}")
    choice = get_menu_selection(len(ASSET_MAP)-1) # -1 for 0 option
    return ASSET_MAP[choice]


TIME_MAP: dict[int, str] = { 1: "15", 
                            2: "60", 
                            3: "240", 
                            4: "D", 
                            5: "W", 
                            0: "None"}

ASSET_MAP: dict[int, str] = { 1: "BTCUSDT", 
                             0: "None"}

