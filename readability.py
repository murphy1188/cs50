from cs50 import get_string

# Initialize variables for letters, words, sentences
letters = 0
words = 1
sentences = 0

# Prompt user for text input
s = get_string("Text: ")

for c in s:
    if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
        letters += 1
    elif " " in c:
        words += 1
    elif "." in c:
        sentences += 1
    elif "?" in c:
        sentences += 1
    elif "!" in c:
        sentences += 1

# Calculate avg number of letters per 100 words
l = 100 / float(words) * letters

# Calculate avg number of sentences per 100 words
x = 100 / float(words) * sentences

# Calculate Coleman-Liau index
index = round((0.0588 * l) - (0.296 * x) - 15.8)

# Output reading level
if index > 0 and index < 17:
    print(f"Grade {index}")
elif index > 16:
    print("Grade 16+")
else:
    print("Before Grade 1")