from Helpers.near_power_helper import show_details


def ask_for_number():
    yn_valid = ('y', 'n')
    
    num = None
    more = None
    table = None
    
    print("Enter a positive integer number to view details about it:")
    while num is None:
        try:
            num = int(input("> "))
        except ValueError:
            print("[!] NaN")
            continue
        
        if num <= 0:
            num = None
            print("[!] Number must be positive integer")
    
    print("Show more info? [YyNn]")

    while more is None:
        more = input("> ").lower()
        
        if more not in yn_valid or more == "":
            more = None
            print("[!] [YyNn]")
    more = True if more == "y" else False
    
    print("Show table? [YyNn]")
    while table is None:
        table = input("> ").lower()
        
        if table not in yn_valid or table == "":
            table = None
            print("[!] [YyNn]")
    table = True if table == "y" else False
    
    show_details(num, more, table)
    
    

if __name__ == '__main__':
    try:
        while True:
            ask_for_number()
    except KeyboardInterrupt:
        ...
    print()
    input("> Press Enter to exit...")
    