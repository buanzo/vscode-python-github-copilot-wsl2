# This is a cabify-expenses script.
# It will use the provided username and password to access a gmail account for emails in a specific label/folder
# related to cabify trips (a filter labels cabify expense reports to a specific folder)
# It will then obtain the Date and Subject of each email in a specific folder.
# It will then parse the Date to extract year and month
# It will then parse the Subject to extract the cost
# It will then add the cost to a dictionary with the key being the year and month
# It will then print the dictionary and other stats

import imaplib
import email
import getpass

# Connect to the gmail server
mail = imaplib.IMAP4_SSL('imap.gmail.com')

# Login to the gmail account
username = input('Enter your gmail username: ')
password = getpass.getpass('Enter your gmail password: ')
mail.login(username, password)

# Print a list of all the imap folders
mail.list()

# Select the folder to search
mail.select('Cabify')

# Search for all emails in the folder
result, data = mail.search(None, 'ALL')

expenses = {}
expenses_per_year = {}
# Loop through each email
for num in data[0].split():
    # Fetch the email
    result, data = mail.fetch(num, '(RFC822)')
    # Convert the email to a string
    raw_email = data[0][1].decode('utf-8')
    # Convert the email to an email object
    email_message = email.message_from_string(raw_email)
    # Print the date and subject of the email
    #print('Date:', email_message['Date'])
    #print('Subject:', email_message['Subject'])
    month = email_message['Date'].split()[2]
    year = email_message['Date'].split()[3]
    key =  f'{year}{month}'
    cost = email_message['Subject'].split('$')[1].replace(',', '')
    print (f"Adding {cost} to {key}")
    if key in expenses:
        expenses[key] += float(cost)
    else:
        expenses[key] = float(cost)
    # Add yearly sums
    if year in expenses_per_year:
        expenses_per_year[year] += float(cost)
    else:
        expenses_per_year[year] = float(cost)

# Round all values to 2 decimals
for key in expenses:
    expenses[key] = round(expenses[key], 2)

for key in expenses_per_year:
    expenses_per_year[key] = round(expenses_per_year[key], 2)

print(expenses)

print(expenses_per_year)

# indicate key from expenses that has highest value
max_key = max(expenses, key=expenses.get)
print(f"Max key is {max_key} with value {expenses[max_key]}")

# Close the connection to the gmail server
mail.close()
mail.logout()
