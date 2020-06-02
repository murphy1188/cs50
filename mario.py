from cs50 import get_int

n = int(get_int("Height: \n"))
while n < 1 or n > 8:
    n = int(get_int("Height: \n"))
for i in range(n + 1):
    print(" " * (n-i), end="")
    print("#" * i, end="")
    print("  ", end="")
    print("#" * (i))
