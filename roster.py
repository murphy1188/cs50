from cs50 import SQL
from sys import argv
from csv import reader
from sys import exit
import csv
import cs50
import sqlite3

# Check command line arguments
# Exit if incorrect number of cmd line args entered
if len(argv) != 2:
    print("Usage: python roster.py house")
    exit(1)
# Link students database
db = SQL("sqlite:///students.db")

# Run query to select name and birth year from house entered in cmnd line arg
house_roster = db.execute("SELECT f, middle, last, birth FROM students WHERE house = ? ORDER BY last, f", argv[1])
for row in house_roster:
    if row['middle'] != None:
        print(f"{row['f']} {row['middle']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['f']} {row['last']}, born {row['birth']}")