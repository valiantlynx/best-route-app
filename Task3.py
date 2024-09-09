# Task 3 -- Simple random search

#Find the triplet $a,b,c \in \{x \;|\; x \in \mathbb{Z} \text{ and } 450 > x > 0 \}$

#Using a random search in the parameter space. Such that the following relations is satisfied:

### a
#$a = \begin{cases} c+11, & \text{if } b\text{ is even} \\ 2c-129, & \text{if } b\text{ is odd} \end{cases}$

### b
#$b = (a \times c) \mod 2377$

### c
#$c = \left( \sum\limits_{k=0}^{a-1} b - 7k \right) + 142$

#**Also how many guesses were needed?**

#Note that in math notation $\sum\limits_{k=1}^{5}k = 1+2+3+4+5$


