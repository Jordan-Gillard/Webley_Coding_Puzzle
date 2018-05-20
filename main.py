import argparse
import os
import csv
import itertools
import sys


def check_if_csv_given(args):
    "checks if the user gave a csv file or if script should ask the user for one."
    
    def get_csv_file_from_user():
        args.csv = input("Please enter the name of the csv to use. Please enter only one csv file at a time. To exit, enter 'quit'.\n")
        if "quit" in args.csv or "Quit" in args.csv:
            sys.exit()
        return args.csv
        
    if not args.csv:
        if isinstance(args.csv, list): #if user typed -csv but didn't specify anything after
            print("Please enter a csv file after using '-csv'.")
            args.csv = get_csv_file_from_user()
        while not os.path.isfile(args.csv):
            args.csv = get_csv_file_from_user()
        args.csv = [args.csv]

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
        if not target_price_row: #checks if the first row is empty
            print('Please check csv file to make sure that the first row is in the format: "target price, value".')
            return False
        if target_price_row[0].lower() != "target price": #checks if the header row has the target price and not a menu item
            print('File header is not properly formatted. The first element of the first row should be "Target price".')
            return False
        target_value = target_price_row[1].strip()
        if target_value[0] != '$':
            print('The value for the target price must begin with "$".')
            return False
        #check if target value converts to a valid floating point number
        try:
            float(target_value[1:])
        except ValueError: 
            print('The target value must be a valid floating point number or integer after the "$" sign, i.e. "$4.50" or "$4".')
            return False
        for row in reader:
            if len(row) != 2 and len(row) != 0:
                print(('This program will skip row: "' + "{},"*len(row) + '" because it is improperly formatted. Rows must be in the format "menu item, price".').format(*row))
    return True
    
def get_target_price(header):
    target_price = header[1].strip()
    target_price_no_currency_sign = target_price[1:]
    target_price_string = "${:.02f}".format(float(target_price_no_currency_sign))
    return target_price_string
    
def check_if_row_is_good(row):
    if not row: #skips empty rows 
        return False
    elif len(row) != 2: #skips improperly formatted rows.
        return False
    try:
        float(row[1].replace('$', ''))
    except:
        print('Skipping row: "{}, {}" because price is improperly formatted.'.format(*row))
        return False
    return True
    
def check_if_there_are_combos_that_match_price(combinations, target_price_string, foods):
    if combinations:
        for combination in combinations:
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
    else:
        print("There are no combinations of menu items that match the target price.")

def run(args):
    for file in args.csv:
        print("Running {}...".format(file))
        if check_csv_file_is_good(file):
            with open(file, 'r') as f:
                reader = csv.reader(f)
                target_price_row = next(reader)
                target_price_string = get_target_price(target_price_row)
                foods = []
                prices = []
                
                for row in reader:
                    if check_if_row_is_good(row):
                        food = row[0]
                        price = float(row[1].replace('$', '')) # $4 => 4.00
                        foods.append(food)
                        prices.append(price)
                        
                enumerated_prices_list = list(enumerate(prices))
                all_possible_combinations_of_prices = [combo for i in range(len(enumerated_prices_list), 0, -1) for combo in itertools.combinations(enumerated_prices_list, i)]
                combinations_that_match_target_price = []
                
                for combination in all_possible_combinations_of_prices:
                    total_price = 0
                    for price in combination:
                        total_price += price[1]
                    total_price_string = "${0:.2f}".format(total_price)
                    if total_price_string == target_price_string:
                        combinations_that_match_target_price.append(combination)
                        
                check_if_there_are_combos_that_match_price(combinations_that_match_target_price, target_price_string, foods)
        print('\n')
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Webley Coding Puzzle. Give a value and find combinations of menu items that equal that value.")
    parser.add_argument("-csv", type=str, nargs='*', default = '', help="csv(s) to parse.")
    args = parser.parse_args()
    
    check_if_csv_given(args)
    run(args)