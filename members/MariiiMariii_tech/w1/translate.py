def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Return all prime numbers up to n.

    Unlike C++, Python uses lists instead of vectors
    and range() instead of traditional for loops.
    """
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False

    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            for i in range(p * p, n + 1, p):
                is_prime[i] = False

    primes = []

    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)

    return primes


print(sieve_of_eratosthenes(20))
