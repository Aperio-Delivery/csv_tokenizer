
## Overview

The script tokenizes selected columns of a CSV file and generates an HTML file with mapping table between the original values and the tokens. This script takes two arguments: CSV filename and a list of comma-separated columns. A list of available column headers will be printed if no column list is provided.

## How to use

To use this script, follow these steps:

1. Open a terminal/command prompt window and navigate to the directory containing the script and CSV file.
2. Type the following command to see the help message and usage instructions:
```html
python tokenize_csv.py -h
```
3. Run the script by typing a command similar to the following:
```
python tokenize_csv.py filename.csv -c Name,Description
```

Replace "filename.csv" with the name of your CSV file, and "Name,Description" with a comma-separated list of column names you want to tokenize. 

After the script finishes running, you should see a message with the summary of what has been done, along with the list of filenames that were created.

## Credits

This code was mostly written by GPT-3.5, prompt is available by request 




