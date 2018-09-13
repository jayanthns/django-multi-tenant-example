import math

prime_numbers = []
x = 2
nthprime = int(input("ENTER A NUMBER\n"))
while len(prime_numbers) < nthprime:
    isPrime = True
    for item in prime_numbers:
        if item > math.log(x):
            break
        if x % item == 0:
            isPrime = False
            break
    if(isPrime):
        primes.append(x)
    x += 1
 
print(prime_numbers[nthprime-1])