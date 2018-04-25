import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def process_sentences(content):
    """tokenizes the text in sentences, removes stop words.
        Args: text - type: list
        Return: text - type: list
     """
    text = " ".join(content)
    word_tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = []
    
    for w in word_tokens:
        if w not in stop_words:
            filtered_words.append(w)
            filtered_sentences = " ".join(filtered_words)
            
    return sent_tokenize(filtered_sentences)


def remove_currency_symbols(text):
    """
    Remove all currency symbols in ``text`` list.
    Args:
        text (list): raw text
    Returns:
        text (list): processed text
    """
    currencies = ['$','zł', '£', '¥', '฿', '₡', '₦', '₩', '₪', '₫', '€', '₱', '₲', '₴', '₹']
    currency_regex = re.compile('({})+'.format('|'.join(re.escape(c) for c in currencies)))
    
    for linenum, line in enumerate(text):
        if currency_regex.search(line) != None:
            text[linenum] = currency_regex.sub('', line)
    
    return text


    
def to_lower(text):
    """Convert the text list to lowercase.
        Args: text - type: list
        Return: text - type: list
    """
    for linenum, line in enumerate(text):
        text[linenum] = line.lower()
        
    return text

def replace_numbers(text, replace_with='*NUMBER*'):
    """Replace all numbers in ``text`` str with ``replace_with`` str.
        Args: text - type: list
        Return: text - type: list
    """
    num_regex = re.compile(r'(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))|(\d+(st|nd|rd|th)\b)')
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
    punctuations = '''!()-–“”’[]{};:'"\,<>./?@#$%^&*_~'''
    
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
        if nonbreaking_space_regex.search(line) != None or linebreak_regex.search(line) != None:
            text[linenum] = nonbreaking_space_regex.sub(' ', linebreak_regex.sub(r'\n', line)).strip()
    
    
    return text
