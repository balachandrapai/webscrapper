import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import nltk

def process_sentences(content):
    """tokenizes the text in sentences, removes stop words.
        Args: text - type: list
        Return: text - type: list
     """
    text = " ".join(content)
    word_tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = []
    processed_sentences = []
    
    for w in word_tokens:
        if w not in stop_words:
            filtered_tokens.append(w)
            
    def get_wordnet_pos(treebank_tag):
        """
        return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v) 
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN
        
        
    def pos_tag(filtered_tokens):
        # find the pos tagging for each tokens [('What', 'WP'), ('can', 'MD'), ('I', 'PRP') ....
        pos_tokens = [nltk.pos_tag(token) for token in filtered_tokens]

        # lemmatization using pos tagg   
        # convert into feature set of [('What', 'What', ['WP']), ('can', 'can', ['MD']), ... ie [original WORD, Lemmatized word, POS tag]
        pos_tokens = [[lemmatizer.lemmatize(word,get_wordnet_pos(pos_tag)) for (word,pos_tag) in pos] for pos in pos_tokens]
        return pos_tokens
    
    lemmatizer = WordNetLemmatizer()
    
    lemma_pos_token = pos_tag([filtered_tokens])
    
    for sentence in lemma_pos_token:
        for w in sentence:
            processed_sentences.append(w)
    
    return sent_tokenize(" ".join(processed_sentences))


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

def remove_numbers(text):
    """Remove all numbers in ``text``
        Args: text - type: list
        Return: text - type: list
    """
    num_regex = re.compile(r'(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))|(\d+(st|nd|rd|th)\b)')
    
    rom_num_regex = re.compile(r'\b(IX|IV|V?I{0,3})\b', re.IGNORECASE)
    
    for linenum, line in enumerate(text):
        if num_regex.search(line) != None:
             text[linenum] = num_regex.sub("", line)
        elif rom_num_regex.search(line) != None:
             text[linenum] = rom_num_regex.sub("", line)
    
    num_regex_greedy = re.compile(r"\d+")
    for linenum, line in enumerate(text):
        if num_regex_greedy.search(line) != None:
             text[linenum] = num_regex_greedy.sub("", line)
    
    return text

def remove_punct(text):
    """ Returns string after removing all the puntuations
        Args: text - type: String
        Return: no_punct - type: String
    """
    # define punctuation
    punctuations = '''!()-–—©䉷∗•…´‘“”`’[]{};:'"\,<>./?@#$%^&*_~'''
    
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

def greedy_removeWords(text):
    """
    Given ``text`` list, replace one or more words with a single char or double.
    This is a greedy approach only used for scientific texts
    """
    
    word_regex = re.compile(r'\b(\w{1}|\w{2})\b')
    
    for linenum, line in enumerate(text):
        if word_regex.search(line) != None:
            text[linenum] = word_regex.sub('', line)
    
    return text

def remove_email(text):
    email_regex = re.compile(r'\b\S*@\S*\s?\b')
    
    for linenum, line in enumerate(text):
        if email_regex.search(line) != None:
            text[linenum] = email_regex.sub('', line)
    
    return text 

def remove_url(text):
    url_regex = re.compile(r'\b(http\S+)|(www\S+)\b')
    
    for linenum, line in enumerate(text):
        if url_regex.search(line) != None:
            text[linenum] = url_regex.sub('', line)
    
    return text
