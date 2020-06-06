from cs50 import SQL
from sys import argv
from csv import reader
from sys import exit
import csv
import cs50

# Check command line arguments
# Exit if incorrect number of cmd line args entered
if len(argv) != 2:
    print("Usage: python import.py csvfile")
    exit(1)

# Create database
open(f"students.db", "w").close()
db = SQL("sqlite:///students.db")

# Create table called 'students' specify columns
db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

# Open CSV file from cmd line arg
with open(argv[1], "r") as characters:
    # Create reader
    reader = csv.DictReader(characters)

    # Iterate over CSV file
    for row in reader:

        # Insert student who have only first/last name
        for name in row["name"].split():
            x = row["name"].split()
        if len(x) == 2:
            db.execute("INSERT INTO students (first, last, house, birth) VALUES(?, ?, ?, ?)", x[0], x[1], row["house"], row["birth"])

        # Insert students who have first/middle/last name
        for name in row["name"].split():
            x = row["name"].split()
        if len(x) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       x[0], x[1], x[2], row["house"], row["birth"])