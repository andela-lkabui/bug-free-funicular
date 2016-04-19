import math

# two is the only even prime number
primes = [2]
# start tracking numbers at 3 (an odd number) to allow
# us to iterate in steps of 2 (since we don't need even numbers)
number = 3
# prime count is 1 because we've taken account of 2 in primes
# list above
prime_count = 1

while True:
	root = math.sqrt(number)
	# assume every number is prime until proven otherwise
	is_a_prime = True

	for prime in primes:
		# Every possible divisor of a number is always less
		# than the square root of that number. We don't need
		# to test numbers that are bigger than the root
		if prime > root:
			break
		# if a number can be divided, it's not a prime
		if number % prime == 0:
			is_a_prime = False
			break

	if is_a_prime:
		primes.append(number)
		prime_count += 1

	if prime_count == 100001:
		break

	number += 2

print('Prime Count: {0}'.format(prime_count))
print('10001st prime: {0}'.format(number))
