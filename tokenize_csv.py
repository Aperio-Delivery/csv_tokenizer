import argparse
import csv
import random
import string
import datetime
import os


timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
token_count = 0 # Initialize token counter
toekn_prefix = ''.join(random.choice(string.ascii_uppercase) for i in range(5))

# Define a function to generate a random 3 uppercase letters followed by an enumerated number
def generate_token():
    global token_count
    token_count+=1
    return toekn_prefix + str(token_count)

# Define a function to read the CSV file and return a list of unique elements for the specified columns
def get_unique_elements(csv_file, columns):
    """Extract unique elements from specified columns in a CSV file"""
    # Open the CSV file
    try:
        with open(csv_file,  encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file}'")
        os.sys.exit(1)

    # Get the column headers from the first row
    headers=[]
    for header in rows[0]:
        headers.append(header.strip())

    # Make sure all specified columns exist
    for column in columns:
        if column not in headers:
            print(f"Error: Column '{column}' not found in CSV file. Available headers are: {headers}")
            os.sys.exit(1)

    # Extract unique elements from the specified columns
    unique_elements = []
    for column in columns:
        for row in rows[1:]:
            element = row[headers.index(column)]
            if element not in unique_elements:
                unique_elements.append(element)

    #print ("Unique elements:", unique_elements)

    return unique_elements


def create_html_table(dict):
    """
    Creates an HTML table with alternating colors between each line and an index from a key-value dictionary
    :param data: A dictionary containing the data to be displayed in the table
    :return: A string representing the HTML table
    """
    html = "<table style='border-collapse: collapse;'>"
    html += "<thead><tr><th>Index</th><th>Element</th><th>Token</th></tr></thead>"
    html += "<tbody>"
    for i, (key, value) in enumerate(dict.items()):
        color = "background-color: #f2f2f2;" if i % 2 == 0 else ""
        html += f"<tr style='{color}'><td>{i}</td><td>{key}</td><td>{value}</td></tr>"
    html += "</tbody></table>"
    return html

# Define a function to tokenize the specified columns in the CSV file
def tokenize_csv(csv_file, columns):
    # Get unique elements for specified columns
    unique_elements = get_unique_elements(csv_file, columns)

    # Generate tokens for unique elements
    tokens = {}
    for element in unique_elements:
        token = generate_token()
        tokens[element] = token

    # Replace elements with tokens in the specified columns and output to a new CSV file
    tokenized_csv = os.path.splitext(csv_file)[0] + "_tokenized_" + timestamp + ".csv"
    try:
        with open(csv_file, encoding='utf-8') as f_in, open(tokenized_csv, 'w', encoding='utf-8', newline='') as f_out:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            #headers = next(reader) # Get column headers

            headers=[]
            for header in next(reader):
                headers.append(header.strip())
                
            writer.writerow(headers) # Write column headers to output file
            for row in reader:
                for col in columns:
                    element = row[headers.index(col)]
                    if element in tokens:
                        row[headers.index(col)] = tokens[element]
                writer.writerow(row)
        print("Successfully tokenized CSV file and output to:", tokenized_csv)
    except Exception as e:
        print("Error tokenizing CSV file:", e)
        os.sys.exit(1)

    # Create an HTML file containing the mapping between elements and tokens
    mapping_html = os.path.splitext(csv_file)[0] + "_mapping_" + timestamp + ".html"
    try:
        html = create_html_table(tokens)
        with open(mapping_html, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Successfully created HTML mapping file:", mapping_html)
    except Exception as e:
        print("Error creating HTML mapping file:", e)

if __name__ == "__main__":
    # Define command line arguments
    parser = argparse.ArgumentParser(description='Tokenize specified columns in a CSV file.')
    parser.add_argument('csv_file', type=str, help='CSV file to tokenize')
    parser.add_argument('-c', '--columns', type=str, help='Comma separated list of columns to tokenize')

    # Parse command line arguments
    args = parser.parse_args()

    # Check if columns argument was specified
    if args.columns:
        columns = args.columns.split(',')
        tokenize_csv(args.csv_file, columns)
    else:
        # Print column headers with their index numbers
        with open(args.csv_file, encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            print("Please specify columns to tokenize using their index numbers:")
            for i, header in enumerate(headers):
                print("{0}: {1}".format(i, header))