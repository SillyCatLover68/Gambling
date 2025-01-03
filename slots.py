import random
import time  

MAX_LINES = 3
MAX_BET = 1000000000000
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    ":3": 2,
    "$": 4,
    ":/": 5,
    ":>": 6
}

symbol_value = {
    ":3": 12,
    "$": 10,
    ":/": 5,
    ":>": 4
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winnings_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)

    return winnings, winnings_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)

    return columns

def print_slot_machine(columns, spin_delay=0.1, final_delay=0.5):
    for _ in range(10):  
        for row in range(len(columns[0])):
            spin_row = " | ".join(random.choice(list(symbol_count.keys())) for _ in columns)
            print(f"\r{spin_row}", end="")  
            time.sleep(spin_delay)
        print("\r", end="")  

    time.sleep(final_delay)
    for row in range(len(columns[0])):
        final_row = " | ".join(column[row] for column in columns)
        print(f"\r{final_row}", end="")  
        time.sleep(0.3)  
        print() 

def deposit():
    while True:
        amount = input("How much would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0!")
        else:
            print("Please enter a valid number.")

    return amount

def get_number_of_lines():
    while True:
        lines = input(f"Enter the number of lines to bet on (1-{MAX_LINES}): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print(f"Please enter a number between 1 and {MAX_LINES}.")
        else:
            print("Please enter a valid number.")

    return lines

def get_bet():
    while True:
        amount = input("How much would you like to bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}!")
        else:
            print("Please enter a valid number.")

    return amount

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"You do not have enough to bet that amount, your current balance: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is equal to: ${total_bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won ${winnings}.")
    print(f"You won on lines:", *winning_lines)
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        answer = input("Press Enter to play (q to quit) ")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You left with ${balance}")

main()
