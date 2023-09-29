import argparse
import re
import random
import os
import chardet
from datetime import datetime

# Define regular expression patterns to match email addresses and phone numbers
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
phone_pattern = r'\b(?:\+\d{1,3}\s*)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b'

# List of 100 motivational quotes
motivational_quotes = [
    "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
    "The only way to do great work is to love what you do.",
    # Add more motivational quotes here
    "Dream big and dare to fail.",
    "Your attitude, not your aptitude, will determine your altitude.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Success is walking from failure to failure with no loss of enthusiasm.",
    "Don't let yesterday take up too much of today.",
    "It does not matter how slowly you go as long as you do not stop."
]

# Function to extract and save email addresses and phone numbers to separate output files
def extract_and_save_info(verbose=False):
    # Get the user's home directory
    home_directory = os.path.expanduser("~")

    # Define the path to the "Leads" folder in the Documents directory
    leads_folder = os.path.join(home_directory, "Documents", "Leads")

    # Create the "Results" folder in the Documents directory if it doesn't exist
    results_folder = os.path.join(home_directory, "Documents", "Results")
    os.makedirs(results_folder, exist_ok=True)

    # Define the desired output file names for emails and phone numbers
    email_output_file_name = input("Enter the desired name for the email output file (e.g., 'emails.txt'): ")
    phone_output_file_name = input("Enter the desired name for the phone number output file (e.g., 'phones.txt'): ")

    # Construct the full paths to the output files
    email_output_file_path = os.path.join(results_folder, email_output_file_name)
    phone_output_file_path = os.path.join(results_folder, phone_output_file_name)

    # Create or clear the email and phone output files
    with open(email_output_file_path, 'w'):
        pass

    with open(phone_output_file_path, 'w'):
        pass

    # Lists to accumulate emails and phones
    all_emails = []
    all_phones = []

    # Iterate through all files in the "Leads" folder
    for idx, entry in enumerate(os.scandir(leads_folder)):
        if entry.is_file():
            try:
                # Detect file encoding using chardet
                detector = chardet.universaldetector.UniversalDetector()
                with open(entry.path, 'rb') as file:
                    for line in file:
                        detector.feed(line)
                        if detector.done:
                            break
                    detector.close()
                    encoding = detector.result['encoding']

                # Reopen the file with detected encoding and read its content
                with open(entry.path, 'r', encoding=encoding, errors='ignore') as file:
                    text = file.read()

                emails = re.findall(email_pattern, text)
                phones = re.findall(phone_pattern, text)

                # Append the email addresses and phones to the respective lists
                all_emails.extend(emails)
                all_phones.extend(phones)

            except Exception as e:
                print(f"Failed to read file '{entry.name}': {e}")
                continue

            # Print progress if verbose mode is enabled
            if verbose:
                print(f"Processed file {idx + 1} of {len(os.listdir(leads_folder))}: {entry.name}")

    # Generate a random motivational quote
    random_quote = random.choice(motivational_quotes)

    # Append the email addresses to the email output file
    with open(email_output_file_path, 'w') as email_file:
        for email in all_emails:
            email_file.write(f"{email}\n")

    # Append the phone numbers to the phone output file
    with open(phone_output_file_path, 'w') as phone_file:
        for phone in all_phones:
            phone_file.write(f"{phone}\n")

    # Print the motivational quote
    print(random_quote)

    # Print the number of emails and phone numbers extracted
    print(f"Number of emails extracted: {len(all_emails)}")
    print(f"Number of phone numbers extracted: {len(all_phones)}")

    # Print the paths of the extracted files
    print(f"Emails saved to: {email_output_file_path}")
