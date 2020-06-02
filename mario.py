from cs50 import get_int

n = int(get_int("Height: "))
while n < 1 or n > 8:
    n = int(get_int("Height: "))
for i in range(n):
    print(" " * (n - (i+1)), end="")
    print("#" * (i + 1), end="")
    print("  ", end="")
    print("#" * (i + 1))
