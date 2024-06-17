import fitz  # PyMuPDF: A Python library for PDF processing
import json  # JSON: A lightweight data interchange format
from extract_courses import *  # Importing all functions from the extract_courses module
from extract_policies import *  # Importing all functions from the extract_policies module

# Path to the PDF file that will be processed
pdf_path = '../incoming_pdf/vt.pdf'

def extract_text_by_page(pdf_path):
    """
    Function to extract text from each page of a PDF file.

    Parameters:
    - pdf_path (str): Path to the PDF document.

    Returns:
    - dict: Dictionary with page numbers as keys and extracted text as values.
    """
    doc = fitz.open(pdf_path)  # Opening the PDF file
    text_by_page = {}  # Initializing an empty dictionary to store text by page
    for page in doc:  # Iterating through each page in the document
        # Extracting text and storing it in the dictionary with page number as key
        text_by_page[page.number] = page.get_text()
    doc.close()  # Closing the document
    return text_by_page  # Returning the dictionary containing text by page

def extract_text_by_line(pdf_path, output_file):
    """
    Function to extract text from a PDF file and write it to an output file, line by line.

    Parameters:
    - pdf_path (str): Path to the PDF document.
    - output_file (str): Path for the output text file.
    """
    doc = fitz.open(pdf_path)  # Opening the PDF file
    text_by_page = {}  # Initializing an empty dictionary to store text by page
    for page in doc:  # Iterating through each page in the document
        blocks = page.get_text("blocks")  # Extracting text blocks from the page
        # Sorting blocks by their vertical, then horizontal position
        sorted_blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
        # Combining text of sorted blocks and storing it in the dictionary
        text_by_page[page.number] = "\n".join([block[4] for block in sorted_blocks])
    doc.close()  # Closing the document

    # Writing the extracted text to the output file, line by line
    with open(output_file, 'w') as file:
        for _, text in text_by_page.items():
            for line in text.splitlines():
                if line.strip():  # Checking if line is not empty
                    file.write(line + "\n")  # Writing the line to the file

def write_to_json(courses_info, filename):
    """
    Function to write course information to a JSON file.

    Parameters:
    - courses_info (dict): Dictionary containing course information.
    - filename (str): Path for the output JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        # Dumping course information into a JSON file with proper formatting
        json.dump(courses_info, file, ensure_ascii=False, indent=4)

# Extracting text by page and storing it in a variable
text_by_page = extract_text_by_page(pdf_path)
# Extracting text by line and writing it to a text file
extract_text_by_line(pdf_path, 'textbyline.txt')

# Extracting course information from the text
courses_info = extract_courses(text_by_page)
# Writing course information to a JSON file
write_to_json(courses_info, "../Flask_Server/backend/data/cdata.json")

# Extracting academic policies from the text file
academic_policies = extract_academic_policies("textbyline.txt")
# Writing academic policies to a JSON file
write_to_json(academic_policies, "../Flask_Server/backend/data/pdata.json")

