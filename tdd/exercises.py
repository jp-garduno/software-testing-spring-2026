# -*- coding: utf-8 -*-

"""
Test Driven Development (TDD) exercises.
"""
import json
import os
import re
import string


def fizzbuzz(num):
    """
    Kata 1 - FizzBuzz

    FizzBuzz is one of the most famous coding exercises for beginners.
    It is a simple exercise but an excellent one to start learning the TDD flow with.

    Requirements
    1. Write a “fizzBuzz” method that accepts a number as input and returns it as a String.

    Notes:

    start with the minimal failing solution
    keep the three rules in mind and always write just sufficient enough code
    do not forget to refactor your code after each passing test
    write your assertions relating to the exact requirements
    2. For multiples of three return “Fizz” instead of the number

    3. For the multiples of five return “Buzz”

    4. For numbers that are multiples of both three and five return “FizzBuzz”.
    """
    output = ""

    if num % 3 == 0:
        output += "Fizz"

    if num % 5 == 0:
        output += "Buzz"

    if output == "":
        output = str(num)

    return output


def _parse_delimiter_and_numbers(numbers):
    """Extract delimiter and number part from input string."""
    if not numbers.startswith("//"):
        return ",", numbers.replace("\n", ",")

    delimiter_end = numbers.find("\n")
    if delimiter_end == -1:
        raise ValueError("Invalid delimiter format")

    delimiter = numbers[2:delimiter_end]
    number_part = numbers[delimiter_end + 1 :]
    return delimiter, number_part


def _collect_validation_errors(numbers, delimiter, number_part):
    """Collect all validation errors for the input."""
    errors = []

    # Check for end separator error
    if number_part.endswith(delimiter):
        errors.append("Input string cannot end with a separator.")

    # Check for invalid delimiter characters (custom delimiters only)
    if numbers.startswith("//"):
        valid_chars = set("0123456789-" + delimiter)
        for i, char in enumerate(number_part):
            if char not in valid_chars:
                errors.append(
                    f"'{delimiter}' expected but '{char}' found at position {i}"
                )
                break

    # Check for negative numbers
    negative_matches = re.findall(r"-\d+", number_part)
    if negative_matches:
        errors.insert(
            0, f"Negative number(s) not allowed: {','.join(negative_matches)}"
        )

    return errors


def add(numbers):
    """
    Kata 2 - String calculator

    Create a simple calculator that takes a String and returns a integer.

    Requirements
    1. The method can take up to two numbers, separated by commas, and will return their sum as a
    result. So the inputs can be: “”, “1”, “1,2”. For an empty string, it will return 0.

    Notes:
    Start with the simplest case (empty string) and extend it with the more advanced cases
    (“1” and “1,2”) step by step keep the three rules in mind and always write just
    sufficient enough code do not forget to refactor your code after each passing test.

    2. Allow the add method to handle an unknown number of arguments.

    3. Allow the add method to handle newlines as separators, instead of comas.
    "1,2\n3" should return "6". "2,\n3" is invalid, but no need to clarify it with the program.

    4. Add validation to not to allow a separator at the end.
    For example "1,2," should return an error (or throw an exception).

    5. Allow the add method to handle different delimiters. To change the delimiter,
    the beginning of the input will contain a separate line that looks like this:
    //[delimiter]\n[numbers]

    Examples:
    - "//;\n1;3" should return "4"
    - "//|\n1|2|3" should return "6"
    - "//sep\n2sep5" should return "7"
    - "//|\n1|2,3" is invalid and should return an error (or throw an exception) with the message
      "'|' expected but ',' found at position 3".

    6. Calling add with negative numbers will return the message:
    "Negative number(s) not allowed: <negativeNumbers>"

    Examples:
    - "1,-2" is invalid and should return the message "Negative number(s) not allowed: -2"
    - "2,-4,-9" is invalid and should return the message "Negative number(s) not allowed: -4,-9"

    7. Calling add with multiple errors will return all error messages separated by newlines.
    "//\n1|2,-3" is invalid and return the message
    "Negative number(s) not allowed: -3\n'|' expected but ',' found at position 3."

    8. Numbers bigger than 1000 should be ignored, so adding 2+1001=2.
    """
    if numbers == "":
        return 0

    try:
        delimiter, number_part = _parse_delimiter_and_numbers(numbers)
    except ValueError as e:
        raise e

    errors = _collect_validation_errors(numbers, delimiter, number_part)

    if errors:
        raise ValueError("\n".join(errors))

    # Parse and sum the numbers (Requirement 8: ignore numbers > 1000)
    num_strings = [s for s in number_part.split(delimiter) if s]
    numbers_list = [int(s) for s in num_strings]
    filtered_numbers = [num for num in numbers_list if num <= 1000]
    return sum(filtered_numbers)


def password_validator(password):
    """
    Kata 3 - Password input field validation

    Create a function that can be used as a validator for the password field of a user registration
    form. The validation function takes a string as an input and returns a validation result.
    The validation result should contain a boolean indicating if the password is valid or not,
    and also a field with the possible validation errors.

    Requirements

    1. The password must be at least 8 characters long.
    If it is not met, then the following error message should be returned:
    "Password must be at least 8 characters".

    2. The password must contain at least 2 numbers.
    If it is not met, then the following error message should be returned:
    "The password must contain at least 2 numbers".

    3. The validation function should handle multiple validation errors.
    For example, "somepassword" should an error message:
    "Password must be at least 8 characters\nThe password must contain at least 2 numbers".

    4. The password must contain at least one capital letter.
    If it is not met, then the following error message should be returned:
    "Password must contain at least one capital letter".

    5. The password must contain at least one special character.
    If it is not met, then the following error message should be returned:
    "Password must contain at least one special character".
    """
    errors = []

    # Requirement 1: Password must be at least 8 characters long
    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    # Requirement 2: Password must contain at least 2 numbers
    number_count = sum(1 for char in password if char.isdigit())
    if number_count < 2:
        errors.append("The password must contain at least 2 numbers")

    # Requirement 4: Password must contain at least one capital letter
    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one capital letter")

    # Requirement 5: Password must contain at least one special character
    if not any(char in string.punctuation for char in password):
        errors.append("Password must contain at least one special character")

    # Return validation result
    is_valid = len(errors) == 0
    return {"is_valid": is_valid, "errors": errors}


def read_from_json(cities_file_name="cities"):
    """Read city names from a JSON file."""
    cities_file_path = os.path.join(
        os.path.dirname(__file__), f"{cities_file_name}.json"
    )
    with open(cities_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data[cities_file_name]


def search_cities(str_to_search):
    """
    Kata 4 - Search functionality

    Implement a city search functionality. The function takes a string (search text) as input
    and returns the found cities which corresponds to the search text.

    Prerequisites:

    Create a collection of strings that will act as a database for the city names.
    City names: Paris, Budapest, Skopje, Rotterdam, Valencia, Vancouver, Amsterdam, Vienna, Sydney,
    New York City, London, Bangkok, Hong Kong, Dubai, Rome, Istanbul.

    Requirements:

    1. If the search text is fewer than 2 characters, then should return no results.
    (It is an optimization feature of the search functionality.)

    2. If the search text is equal to or more than 2 characters, then it should return all the city
    names starting with the exact search text.
    For example for search text "Va", the function should return Valencia and Vancouver.

    3. The search functionality should be case insensitive.

    4. The search functionality should work also when the search text is just a part of a city name
    For example "ape" should return "Budapest" city.

    5. If the search text is a "*" (asterisk), then it should return all the city names.
    """
    # Load cities from JSON file
    cities = read_from_json("cities")
    cities_found = []

    # Requirement 5: If search text is "*", return all cities
    if str_to_search == "*":
        return cities

    # Requirement 1: If search text is fewer than 2 characters, return no results
    if len(str_to_search) < 2:
        return cities_found

    # Convert search text to lowercase for case-insensitive search (Requirement 3)
    search_lower = str_to_search.lower()

    for city in cities:
        city_lower = city.lower()
        # Requirement 2: Cities starting with search text
        # Requirement 4: Cities containing search text (substring search)
        if city_lower.startswith(search_lower) or search_lower in city_lower:
            cities_found.append(city)

    return cities_found


def scan_barcode(barcode):
    """
    Kata 5: Point of sale

    Create a simple app for scanning bar codes to sell products.

    Requirements:

    1. Barcode '12345' should display price '$7.25'.

    2. Barcode '23456' should display price '$12.50'.

    3. Barcode '99999' should display 'Error: barcode not found'.

    4. Empty barcode should display 'Error: empty barcode'.

    5. Introduce a concept of total command where it is possible to scan multiple items.
    The command would display the sum of the scanned product prices.
    """
    # Requirement 4: Empty barcode should display 'Error: empty barcode'
    if not barcode or barcode.strip() == "":
        return "Error: empty barcode"

    # Load product database from JSON file
    products = read_from_json("products")

    # Check if barcode exists in products database
    if barcode in products:
        return products[barcode]

    # Requirement 3: Unknown barcode should display 'Error: barcode not found'
    return "Error: barcode not found"
