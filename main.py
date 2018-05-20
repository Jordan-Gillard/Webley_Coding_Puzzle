import argparse
import os.path
import csv
import itertools
from pprint import pprint #delete this later

parser = argparse.ArgumentParser(description="Webley Coding Puzzle. Give a value and find combinations of menu items that equal that value.")
parser.add_argument("-csv", type=str, nargs='*', default = '', help="csv(s) to parse.")
args = parser.parse_args()

if not args.csv:
    while not os.path.isfile(args.csv):
        args.csv = input("Please enter the name of the csv to use. To exit, enter 'quit'.\n")
        if args.csv.lower() == 'quit':
            break
        
for file in args.csv:
    with open (file, 'r') as f:
        reader = csv.reader(f)
        target_price_row = next(reader)
        target_price_string = target_price_row[1].strip()
        foods = []
        prices = []
        for row in reader:
            if not row: #skips empty rows 
                pass
            elif len(row) < 2 or len(row) > 2: #skips improperly formatted rows.
                print(('skipped row: "' + "{},"*len(row) + '" because it is improperly formatted.').format(*row))
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
        
    