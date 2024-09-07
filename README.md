# Web Site Admin Page Scanner

## Description

This Python script performs a scan on a given domain to detect redirected pages. After the scan is complete, it searches the pages using a provided word list to find potential admin panels and other important pages.

## Features

- Domain scanning and detection of redirected pages
- Searching web pages with specific words
- Saving results to a file
- User-friendly language selection and loading animation

## Requirements

To run this script, you need to install the following Python packages:

- `requests`
- `beautifulsoup4`
- `tldextract`

Install the required packages using:

```sh
pip install -r requirements.txt
```

- Download the Script: Download or clone the repository containing the script.

- Install Dependencies: Ensure you have Python installed, then install the required packages using the command above.

- Run the Script:
```sh
python scanner.py
```
- Follow the Prompts:

- Language Selection: Choose between English or Turkish by entering 1 for English or 2 for Turkish.
- Domain Input: Enter the domain you want to scan (e.g., example.com).
- Word List File: After the scan, you will be prompted to enter the path to the word list file (e.g., wordlist.txt).

- Check Results:

- Scanned pages will be saved to site_page.txt.
- Results of the word list search will be saved to found_admin_pages.txt.


## Author

Created by **who0ze**  
GitHub: [https://github.com/who0ze](https://github.com/who0ze)

## License
- This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for details.
