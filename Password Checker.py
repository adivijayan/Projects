# Check If Your Password Has Been Exposed In A Data Leak
# This program uses the SHA1 algorithm to hash the password you enter. 
# The first 5 characters of that hash are then sent to the pwnedpasswords API, which sends back the "tails" of the hashes (the remaining characters after the first 5 have been matched)
# To ensure that your actual password(hashed and not) is not sent to the internet, your hash and the exposed hashes (the first 5 characters of which match your hashed password's first 5) are
# compared on your system. If there is a match in the database, then the program prints how many times it has been found.
import requests
import hashlib
import sys


def request_api_date(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching {res.status_code}, check the API and try again.")
    return res


def get_pwd_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_date(first5_char)
    return get_pwd_leaks_count(response, tail)


if __name__ == "__main__":
    while True:
        password = input("Enter a password to check if it has been leaked on the internet (or 'exit' to quit): ")
        if password.lower() == "exit":
            break
        count = pwned_api_check(password)
        if count:
            print(f"'{password}' was found {count} times... Consider changing your password.")
        else:
            print(f"'{password}' was NOT found in the database. Good job!")
