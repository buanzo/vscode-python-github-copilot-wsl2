import sys
import subprocess
import pyasn  # this i added by myself

asndb = pyasn.pyasn('latest.asn')    # this i added by myself

# This script reads the file fail2ban.log from the current directory.
# It extract IP addresses from each line and saves them to a list.
def get_ip_list(logfile):
    # Open the file for reading.
    with open(logfile, 'r') as f:
        # Create an empty list.
        ip_list = []
        # Loop over each line in the file.
        for line in f:
            # Split the line into a list of words.
            words = line.split()
            # Loop over each word in the list.
            for word in words:
                # Check if the word is an IP address, and if it is not already in the list.
                if is_ip(word) and word not in ip_list:
                    # Add the IP address to the list.
                    ip_list.append(word)
    # Return the list of IP addresses.
    return(ip_list)

# This function checks if a string is an IP address.
def is_ip(s):
    # Split the string into a list of numbers.
    numbers = s.split('.')
    # Check if the list has 4 elements.
    if len(numbers) != 4:
        return False
    # Loop over each number in the list.
    for number in numbers:
        # Check if the number is an integer.
        if not number.isdigit():
            return False
        # Convert the number to an integer.
        i = int(number)
        # Check if the number is between 0 and 255.
        if i < 0 or i > 255:
            return False
    # The string is an IP address.
    return True


# For each ip in ips:
# 1. Obtain associated AS number and save to a dictionary as key
# 2. Save the IP address to the value list of the dictionary
# 3. Print the dictionary
def create_as_dictionary(ips):
    # Create an empty dictionary.
    as_dict = {}
    # Loop over each ip in ips.
    for ip in ips:
        # Obtain the AS number from ip.
        as_num = get_as_number(ip)
        # Check if the AS number is already in the dictionary.
        if as_num in as_dict:
            # Add the IP address to the list of IP addresses.
            as_dict[as_num].append(ip)
        else:
            # Create a new list containing the IP address.
            as_dict[as_num] = [ip]
    # Return the dictionary.
    return(as_dict)

def get_as_number(ip):
    return(asndb.lookup(ip)[0] or 'Unknown')

# This function takes a dictionary and returns it sorting the keys by number of items per key, with the most items first.
def sort_dict_by_value(d):
    return(sorted(d.items(), key=lambda x: len(x[1]), reverse=True))

def main():
    if len(sys.argv) == 2:
        logfile = sys.argv[1]
    else:
        logfile = 'fail2ban.log'

    ips = get_ip_list(logfile)
    # Create the dictionary.
    as_dict = create_as_dictionary(ips)
    # Print the dictionary.
    as_dict = sort_dict_by_value(as_dict)
    print('AS Number', 'Number of IPs', 'IPs')
    for as_num, ip_list in as_dict:
        print(as_num, len(ip_list), ip_list)

if __name__ == '__main__':
    main()

