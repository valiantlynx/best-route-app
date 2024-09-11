import random


def finnC():
    n = 0
    while True:
        n += 1
        if n >= 100000:
            print("Ingen løsning funnet etter {n}".format(n=n)),"forsøk."
            break
        c = random.randint(1, 449)

        if c % 2 == 0:
            a = c + 11
        else:
            a = 2 * c - 129

        b = (a * c) % 2377

        sum_result = sum([b - 7 * k for k in range(a)])
        new_c = sum_result + 142

        if new_c == c:
            print(f"Løsning funnet etter {n} iterasjoner.")
            print(f"a = {a}, b = {b}, c = {c}")
            break


finnC()
