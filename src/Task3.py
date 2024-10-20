import random

def find_triplet():
    n = 0
    while True:
        n += 1
        if n > 1000000:
            print(f"No solution found after {n} attempts.")
            break

        #have to generate a random C to calculate A.
        c = random.randint(1, 449)

        #Calculate A before knowing if B is odd or even.
        a_even = c + 11
        a_odd = 2 * c - 129

        #check if A is between 0 and 450.
        if 0 < a_even < 450:
            a = a_even
            # Calculate B based on A and C.
            b = (a * c) % 2377
            #check if B is Even. If it is: calculate new_C.
            if b % 2 == 0 and 0 < b < 450:
                #the condition that C needs to meet.
                sum_result = sum([b - 7 * k for k in range(a)])
                new_c = sum_result + 142
                #Check if we have found a solution. C = new_c
                if new_c == c:
                    print(f"Solution found after {n} iterations:")
                    print(f"a = {a}, b = {b}, c = {c}")
                    break

        ##check if A is between 0 and 450.
        if 0 < a_odd < 450:
            a = a_odd
            #Calculate B based on A and C.
            b = (a * c) % 2377
            #check if B is Even. If it is: Calculate new_C.
            if b % 2 == 1 and 0 < b < 450:
                # the condition that C needs to meet.
                sum_result = sum([b - 7 * k for k in range(a)])
                new_c = sum_result + 142
                #Check if solution is found.
                if new_c == c:
                    print(f"Solution found after {n} iterations:")
                    print(f"a = {a}, b = {b}, c = {c}")
                    break

find_triplet()
