import time

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CLEAR = "\033[2J\033[3J\033[H"


def display_msg(msg, change_line=False, wait=False, color=Colors.BLUE):
    print(f" {color}{Colors.BOLD}{msg}{Colors.RESET}", end="\n" if change_line else "")
    if wait:
        time.sleep(2)


def display_menu(items, instruction, head, clear):
    if clear:
        print(Colors.CLEAR, end="")

    line_hor = "─"

    if head:
        print(f"\n {Colors.CYAN}{Colors.BOLD}{head.upper()} {Colors.RESET}")
        print(f" {Colors.DIM}{line_hor * len(head)}{Colors.RESET}\n")

    valid_keys = [chr(49 + i) for i in range(len(items))]

    for i, option in enumerate(items):
        key = valid_keys[i]
        print(f" {Colors.BLUE}[{key}]{Colors.RESET} {option}")

    if instruction:
        print(f"\n {Colors.YELLOW}{instruction}{Colors.RESET}\n")

    while True:
        try:
            choice = input(f"\n {Colors.GREEN}>>> {Colors.RESET}").strip().lower()
            if choice in valid_keys:
                return ord(choice) - ord('0')
            else:
                print(f" {Colors.RED}Enter Valid Choice!{Colors.RESET}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n {Colors.RED}Exiting...{Colors.RESET}")
            exit()