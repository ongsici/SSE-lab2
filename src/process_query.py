import math


def is_square(n):
    return int(math.sqrt(n)) ** 2 == n


def is_cube(n):
    return int(round(n ** (1/3))) ** 3 == n


def is_prime(n):
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def process_query(input):
    plus_count = input.count("plus")
    if plus_count == 2:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input.split(" ")[4])
        value3 = int(new_input.split(" ")[6])
        return str(value1+value2+value3)

    if "numbers are primes" in input:
        input = input.replace("?", "")
        value = input.split(":")[-1].split(",")
        result = []
        for number in value:
            number = number.strip()
            if is_prime(int(number)):
                result.append(number)
        return ",".join(result)

    if "minus" in input:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input.split(" ")[4])
        return str(value1-value2)

    if "multiplied by" in input:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input.split(" ")[5])
        return str(value1*value2)

    if "square and a cube" in input:
        input = input.replace("?", "")
        value = input.split(":")[-1].split(",")
        result = []
        for number in value:
            number = number.strip()
            if is_square(int(number)) and is_cube(int(number)):
                result.append(number)
        return ",".join(result)

    if plus_count == 1:
        new_input = input.replace("?", "")
        value1 = int(new_input.split(" ")[2])
        value2 = int(new_input.split(" ")[4])
        return str(value1+value2)

    if "numbers is the largest" in input:
        input = input.replace("?", "")
        value = input.split(":")[-1].split(",")
        return max(value)

    if "your name" in input:
        return "SiCi"

    if input == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    else:
        return "Unknown"

