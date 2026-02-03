import pyfiglet


def menu_runner(title: str, options: dict[int, list], header: str, args: list) -> None:
    menu_length: int =  len(options) + 1 
    while True:
        print_banner(title)
        dynamic_fprint(header, args)

        for key, (label, _) in options.items():
            print(f"{key}. {label}")
        print(f"{menu_length}. Exit")

        choice = get_menu_selection(menu_length)

        if choice == menu_length:
            return

        _, func = options[choice]

        func


def print_banner(banner_text:str="Algorithmic Trading SYS") -> None:
    """
    Clears the terminal display and prints a banner for the current menu
           
    Args:
        banner_text: The text to print inside the banner, default to app name.
    """
    print("\033c", end="")
    text = pyfiglet.figlet_format(banner_text, font="slant")
    print(text)
    print("-"*60)


def dynamic_fprint(template:str, *args:list):
    if template == "":
        return
    print(template.format(*args))

    
def get_menu_selection(options:int) -> int:
    """ Returns the selected menu item """
    print("-"*60)
    while True:
        try:
            choice = int(input("\n>> "))
        except (ValueError, TypeError):
            print("Enter a number from the provided options")
            continue

        if choice > 0 and choice < options+1:
            return choice 
        print("Enter a number from the provided options")


TIME_MAP: dict[int, str] = { 1: "15", 
                            2: "60", 
                            3: "240", 
                            4: "D", 
                            5: "W", 
                            0: "None"}

ASSET_MAP: dict[int, str] = { 1: "BTCUSDT", 
                             0: "None"}
