import random

def find_triplet():
    n = 0
    while True:
        n += 1
        if n > 1000000:
            print(f"No solution found after {n} attempts.")
            break

        c = random.randint(1, 449)
        a_even = c + 11
        a_odd = 2 * c - 129

        if 0 < a_even < 450:
            a = a_even
            b = (a * c) % 2377
            if b % 2 == 0 and 0 < b < 450:
                sum_result = sum([b - 7 * k for k in range(a)])
                new_c = sum_result + 142
                print(sum_result)
                print(new_c)
                if new_c == c:
                    print(f"Solution found after {n} iterations:")
                    print(f"a = {a}, b = {b}, c = {c}")
                    break

        if 0 < a_odd < 450:
            a = a_odd
            b = (a * c) % 2377
            if b % 2 == 1 and 0 < b < 450:
                sum_result = sum([b - 7 * k for k in range(a)])
                new_c = sum_result + 142
                print(sum_result)
                print(new_c)
                if new_c == c:
                    print(f"Solution found after {n} iterations:")
                    print(f"a = {a}, b = {b}, c = {c}")
                    break

find_triplet()
