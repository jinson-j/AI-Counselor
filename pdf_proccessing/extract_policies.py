def extract_academic_policies(filename):
    """
    Extracts academic policies from a given file and organizes them into a structured dictionary.
    
    Args:
    filename (str): The path to the file containing academic policies.
    
    Returns:
    dict: A dictionary with a key "University Policies" containing a list of policies, 
          each policy represented as a dictionary with the policy title and its explanation.
    """
    # Initialize a dictionary to hold the extracted academic policies
    academic_policies = {"University Policies": []}
    
    # Open and read the file line by line
    with open(filename, 'r') as file:
        lines = file.readlines()
        
        # Initialize a counter to iterate through the lines of the file
        i = 0
        while i < len(lines):
            # Check if the current line marks the beginning of an academic policy section
            if lines[i].strip() == "Academic Policies":
                # Skip the next 3 lines (usually headers or empty lines)
                i += 3
                # Continue until the next occurrence of "Academic Policies" or end of file
                while i < len(lines) and lines[i].strip() != "Academic Policies":
                    # Extract the title of the academic policy
                    title = lines[i].strip()
                    i += 1
                    # Initialize a list to hold the lines of the policy explanation
                    values = []
                    # Continue extracting lines until the next policy section or end of file
                    while i < len(lines) and lines[i].strip() != "Academic Policies":
                        values.append(lines[i].strip())
                        i += 1
                    # Concatenate the extracted lines into a single string to form the policy explanation
                    values_concatenated = ' '.join(values)
                    # Append the extracted policy to the list of policies in the dictionary
                    academic_policies["University Policies"].append({"Title of Academic Policy": title, "University Academic Policy Explained": values_concatenated})
            else:
                # Move to the next line if the current line is not the beginning of a policy section
                i += 1
    # Return the dictionary containing all extracted academic policies
    return academic_policies