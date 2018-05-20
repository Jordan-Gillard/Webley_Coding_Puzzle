# Webley Coding Puzzle

### About
This script parses one or multiple csv files. In order for it to properly work, the first line of each csv file must be in the format "Target price,value", i.e. `Target price, $15.05`. The following rows should be in the format "menu item, price", i.e. `mixed fruit,$2.15`. The script checks all combinations of menu items to see if they add up to the target price. If they do, then that result is printed out to the user. If no combinations exist, the script prints that to the user as well.  

### How to use
There are two ways to use this:  
&nbsp;&nbsp;&nbsp;&nbsp;1. You can simply type on the command line `python main.py` to get started. This route will prompt you to enter a file.  
&nbsp;&nbsp;&nbsp;&nbsp;2. or you can specify one, or multiple, csv files by typing on the command line `python main.py -csv file_1.csv file_2.csv`
  
Please note that if you want to enter multiple files, you have to use `-csv` on the command line.