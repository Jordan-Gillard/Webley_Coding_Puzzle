import argparse
import os
import csv
import itertools
import sys
from pprint import pprint #delete this later

parser = argparse.ArgumentParser(description="Webley Coding Puzzle. Give a value and find combinations of menu items that equal that value.")
parser.add_argument("-csv", type=str, nargs='*', default = '', help="csv(s) to parse.")
args = parser.parse_args()

if not args.csv:
    while not os.path.isfile(args.csv):
        args.csv = input("Please enter the name of the csv to use. To exit, enter 'quit'.\n")
        if args.csv.lower() == 'quit':
            sys.exit()

def check_that_csv_file_exists(file):
    if os.path.isfile(file):
        return
    print("Please enter a valid csv file and try again.")
    sys.exit()

def check_csv_file_is_good(file):
    check_that_csv_file_exists(file)
    if os.stat(file).st_size == 0: #checks if csv is empty
        print("File contains no data. Please use a different file.")
        return False
    with open(file, 'r') as f:
        reader = csv.reader(f)
        target_price_row = next(reader)
        if target_price_row[0].lower() != "target price": #checks if the header row has the target price and not a menu item
            print('File header is not properly formatted. The first element of the first row should be "Target price".')
            return False
        target_value = target_price_row[1].strip()
        if target_value[0] != '$':
            print('The value for the target price must begin with "$".')
            return False
        #check if target value is valid
        try:
            float(target_value[1:])
        except ValueError: 
            print('The target value must be a valid floating point number or integer, i.e. "$4.50" or "$4".')
            return False
        for row in reader:
            if len(row) != 2 and len(row) != 0:
                print(('This program will skip row: "' + "{},"*len(row) + '" because it is improperly formatted. Rows must be in the format "menu item, price".').format(*row))
    return True
        
for file in args.csv:
    if check_csv_file_is_good(file):
        with open(file, 'r') as f:
            reader = csv.reader(f)
            target_price_row = next(reader)
            target_price = target_price_row[1].strip()
            target_price_no_currency_sign = target_price[1:]
            target_price_string = "${:.02f}".format(float(target_price_no_currency_sign))
            foods = []
            prices = []
            for row in reader:
                if not row: #skips empty rows 
                    pass
                elif len(row) != 2: #skips improperly formatted rows.
                    pass
                    # print(('skipped row: "' + "{},"*len(row) + '" because it is improperly formatted.').format(*row))
                else:
                    food = row[0]
                    price = float(row[1].replace('$', ''))
                    foods.append(food)
                    prices.append(price)
            enumerated_foods_list = list(enumerate(foods))
            enumerated_prices_list = list(enumerate(prices))
            all_possible_combinations_of_prices = [combo for i in range(len(enumerated_foods_list), 0, -1) for combo in itertools.combinations(enumerated_prices_list, i)]
            combinations_that_match_target_price = []
            for combination in all_possible_combinations_of_prices:
                total_price = 0
                for price in combination:
                    total_price += price[1]
                total_price_string = "${0:.2f}".format(total_price)
                if total_price_string == target_price_string:
                    combinations_that_match_target_price.append(combination)
            for combination in combinations_that_match_target_price:
                message_to_user = ""
                for menu_item in combination:
                    item = menu_item[0]
                    price = menu_item[1]
                    dish_name = foods[item]
                    message_to_user += '{} at ${:.02f}'.format(dish_name, price)
                    if len(combination) != 1:
                        message_to_user += ', '
                    else:
                        message_to_user += ' '
                message_to_user += "is equal to the target price of {}.".format(target_price_string)
                
                print(message_to_user)
            
        