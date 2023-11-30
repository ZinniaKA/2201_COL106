import random
import math

# To generate a random prime less than N
def randPrime(N):
    primes = []
    for q in range(2, N + 1):
        if isPrime(q):
            primes.append(q)
    return primes[random.randint(0, len(primes) - 1)]

# To check if a number is prime
def isPrime(q):
    if q > 1:
        for i in range(2, int(math.sqrt(q)) + 1):
            if q % i == 0:
                return False
        return True
    else:
        return False

# Pattern matching
def randPatternMatch(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatch(q, p, x)

# Pattern matching with a wildcard
def randPatternMatchWildcard(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatchWildcard(q, p, x)

# Return the appropriate N that satisfies the error bounds
def findN(eps, m):
    return (2 * m / eps * math.log2(26)) * (2 * m / eps * math.log2(26)) * eps

# Function to return a sorted list of starting indices where p matches x
def modPatternMatch(q, p, x):
    n = len(x)
    m = len(p)
    ans = []  # Final output list
    factor = 1
    constant = 26 % q
    remainder = 0
    match = 0

    if n >= m:
        for i in range(m - 1, -1, -1):
            remainder = (remainder + ((ord(x[i]) - 65) % q) * factor) % q
            match = (match + ((ord(p[i]) - 65) % q) * factor) % q
            factor = (factor * constant) % q

        for i in range(0, n - m):
            if match == remainder:
                ans.append(i)
            remainder = (
                (remainder * constant) % q
                + (ord(x[i + m]) - 65) % q
                - (((ord(x[i]) - 65) % q) * factor) % q
            ) % q
            if remainder < 0:
                remainder += q
        if match == remainder:
            ans.append(n - m)
    return ans

# Function to return pattern matching in case of a wildcard element ?
def modPatternMatchWildcard(q, p, x):
    n = len(x)
    m = len(p)
    ans = []
    factor = 1
    constant = 26 % q
    remainder = 0
    match = 0
    wild = 1

    if n >= m:
        k = p.index("?")
        for i in range(0, m-k-1):
            wild = (wild * constant) % q

        for i in range(m - 1, -1, -1):
            remainder = (remainder + ((ord(x[i]) - 65) % q) * factor) % q
            match = (match + ((ord(p[i]) - 65) % q) * factor) % q
            factor = (factor * constant) % q

        match = (
            match - (wild * ((ord(p[k]) - 65) % q)) % q
            if match - (wild * ((ord(p[k]) - 65) % q)) % q >= 0
            else match - (wild * ((ord(p[k]) - 65) % q)) % q + q
        )
        for i in range(0, n - m):
            remainder_ = (
                remainder
                - (wild * ((ord(x[i + k]) - 65) % q)) % q
                if remainder - (wild * ((ord(x[i + k]) - 65) % q)) % q >= 0
                else remainder - (wild * ((ord(x[i + k]) - 65) % q)) % q + q
            )
            if match == remainder_:
                ans.append(i)
            remainder = (
                (remainder * constant) % q
                + (ord(x[i + m]) - 65) % q
                - (((ord(x[i]) - 65) % q) * factor) % q
            ) % q
            if remainder < 0:
                remainder += q
        remainder_ = (
            remainder
            - (wild * ((ord(x[n - m + k]) - 65) % q)) % q
            if remainder - (wild * ((ord(x[n - m + k]) - 65) % q)) % q >= 0
            else remainder - (wild * ((ord(x[n - m + k]) - 65) % q)) % q + q
        )
        if match == remainder_:
            ans.append(n - m)
    return ans