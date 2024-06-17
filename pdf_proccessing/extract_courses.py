import re

def find_course_info(course_code, text_by_page):
    """
    Searches for a specific course's information within a given text, organized by page numbers.
    
    Args:
    course_code (str): The specific course code to search for.
    text_by_page (dict): A dictionary with page numbers as keys and page text as values.
    
    Returns:
    tuple: A tuple containing the course description and the page number where it was found. 
           Returns ("Course not found", None) if the course is not found.
    """
    # Compile a regex pattern to isolate a course's description, stopping at the next course's code or end of text
    course_pattern = re.compile(rf"(\b{course_code}\b.+?)(?=\b[A-Z]+\s+\d+\.|\Z)", re.DOTALL)
    
    for page_number, text in text_by_page.items():
        match = course_pattern.search(text)
        if match:
            # Clean the matched text and remove line breaks for a continuous description
            course_description = match.group(1).strip()
            course_description = ' '.join(course_description.split('\n'))
            return course_description, page_number
    return "Course not found", None

def extract_courses(text_by_page):
    """
    Extracts courses and their details from given text, organized by page numbers.
    
    Args:
    text_by_page (dict): A dictionary with page numbers as keys and page text as values.
    
    Returns:
    dict: A dictionary containing a list of courses, each represented as a dictionary with course details.
    """
    courses_list = []  # Initialize a list to store course details
    # Compile a regex pattern to capture course details, including an optional credits section
    course_pattern = re.compile(r"(\d{4}): ([^\n]+)\n(.*?)(\(\d+H,\d+C\))?(?=\d{4}:|\Z)", re.DOTALL)

    for page_number, text in text_by_page.items():
        for match in course_pattern.finditer(text):
            course_id = match.group(1).strip()
            course_title = match.group(2).strip()
            course_description = match.group(3).strip()

            # Attempt to find and separate the credits information from the course description
            credits_search = re.search(r'\((\d+H,\d+C)\)$', course_description)
            if credits_search:
                course_credits = credits_search.group(1)
                course_description = re.sub(r'\s*\(\d+H,\d+C\)$', '', course_description)
            else:
                course_credits = "Variable"
            
            # Add course details to the list if the course title is in all caps (indicating a valid course entry)
            if course_title.isupper():
                courses_list.append({
                    "course_name": course_title,
                    "course_id": course_id,
                    "course_description": course_description.strip(),
                    "course_credits": course_credits
                })
    
    return {"courses": courses_list}  # Wrap the list of courses in a dictionary under the key "courses"
