import re

def replace_numbers(text, replace_with='*NUMBER*'):
    """Replace all numbers in ``text`` str with ``replace_with`` str.
        Args: text - type: list
        Return: text - type: list
    """
    num_regex = re.compile(r'(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))')
    for linenum, line in enumerate(text):
        if num_regex.search(line) != None:
             text[linenum] = num_regex.sub(replace_with, line)
            
    return text

def strip_punct(text):
    """ Returns string after removing all the puntuations
        Args: text - type: String
        Return: no_punct - type: String
    """
    # define punctuation
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    
    no_punct = ""
    for char in text:
        if char not in punctuations:
            no_punct = no_punct + char

    # return the unpunctuated string
    return no_punct


def normalize_whitespace(text):
    """
    Given ``text`` list, replace one or more spacings with a single space, and one
    or more linebreaks with a single newline. Also strip leading/trailing whitespace.
    """
    nonbreaking_space_regex = re.compile(r'(?!\n)\s+')
    linebreak_regex = re.compile(r'((\r\n)|[\n\v])+')
    
    for linenum, line in enumerate(text):
        if nonbreaking_space_regex.search(line) != None or linebreak_regex.search(line):
            text[linenum] = nonbreaking_space_regex.sub(' ', linebreak_regex.sub(r'\n', line)).strip()
    
    
    return text
