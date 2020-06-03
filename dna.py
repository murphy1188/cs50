from sys import argv
from csv import reader
import re
import csv
import sys

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit(1)
# Open dna database and read into list of lists
with open(argv[1], "r") as csv_file:
    dna_database = list(reader(csv_file))
# Set variables for STR counter, STR max Counter, STR Length
STR_Counter = []
STR_Max_Count = []
STR = []
STR_Length = []
# Makes lists long enough for imported files
for i in range(len(dna_database[0])):
    STR_Counter.append(i)
    STR_Max_Count.append(i)
    STR.append(dna_database[0][i])
    STR_Length.append(i)
# Set variables to 0 
for i in range(len(dna_database[0])):
    STR[i] = dna_database[0][i]
    STR_Counter[i] = 0
    STR_Max_Count[i] = 0
    STR_Length[i] = len(dna_database[0][i])
# Open dna sequence to test
with open(argv[2], "r") as sequence_file:
    sequence = str(sequence_file.read())
    length = len(sequence)
# Check sequence for max consecutive STRs
for k in range(length):
    for i in range(len(dna_database[0])):
        if sequence[k:(k + STR_Length[i])] == STR[i] and sequence[(k + STR_Length[i]):(k + (2 * STR_Length[i]))] == STR[i]:
            STR_Counter[i] += 1
        if (STR_Counter[i]) >= (STR_Max_Count[i]):
            STR_Max_Count[i] = STR_Counter[i]
        if sequence[k:(k + STR_Length[i])] == STR[i] and sequence[(k + STR_Length[i]):(k + (2 * STR_Length[i]))] != STR[i]:
            STR_Counter[i] = 0

for i in range(1, len(dna_database[0])):
    STR_Max_Count[i] += 1
# Creat list of Max Counts of consecutive STRs in same format as DNA Database
sequence_data = []
for i in range(1, len(dna_database[0])):
    sequence_data.append(f"{STR_Max_Count[i]}")

# Check for match from sequence against DNA Database
match = 0
for i in range(len(dna_database)):

    if sequence_data[0:len(dna_database[0])] == dna_database[i][1:len(dna_database[0])]:
        print(dna_database[i][0])
        match += 1
if match == 0:
    print("No match")