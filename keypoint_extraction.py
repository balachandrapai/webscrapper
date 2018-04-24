import os
import sys
import re
import logging

#logging each level
logger = logging.getLogger('text_extraction')
hdlr = logging.FileHandler('d:\\text_extraction.txt')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

def get_startIndex(file):
    """
    Args:
        file : file for which the starting index is supposed to be obtained

    Returns:
        start index for extraction
    """
    
    startIndex = 0
    
    start_word = re.compile(r"\bSUMMARY\b", re.IGNORECASE)
    
    logger.info('Getting the start index')
    
    for linenum, line in enumerate(file):
        if start_word.search(line) != None:
            startIndex = linenum
    
    return startIndex

def get_endIndex(file):
    
    """
    Args:
        file : file for which the ending index is supposed to be obtained

    Returns:
        end index for extraction
    
    """
    
    endIndex, endPattern1, endPattern2, endPattern3, endPattern4, endPattern5 = len(file), len(file), len(file), len(file), len(file), len(file)
    
    logger.info('Getting the end index')
    
    for linenum, line in enumerate(file):
        if re.match(r"WHEN.*APPLY\?\n", line) != None:
            endPattern1 = linenum
        elif re.match(r"WHEN.*IMPLEMENTED\?\n", line) != None:
            endPattern2 = linenum
        elif re.match(r"WHEN.*FORCE\?\n", line) != None:
            endPattern3 = linenum
        elif re.match(r"RELATED.*", line) != None:
            endPattern4 = linenum
        elif re.match(r"DATE.*FORCE", line) != None:
            endPattern5 = linenum
        else:
            endIndex = endIndex
        
        
    
    return min(endIndex, endPattern1, endPattern2, endPattern3, endPattern4, endPattern5)

def remove_extras(file):
    """
    Args:
        file : file for which the ending index is supposed to be obtained

    Returns:
        end index for extraction
    
    """
    
    endIndex, endPattern1, endPattern2 = len(file), len(file), len(file)
    
    logger.info('Checking for extras and getting the end index')
    
    for linenum, line in enumerate(file):
        if re.match(r"References\n", line) != None:
            endPattern1 = linenum
        elif re.match(r"See also\n", line) != None:
            endPattern2 = linenum
        else:
            endIndex = endIndex
                   
    return min(endIndex, endPattern1, endPattern2)

walk_dir = "d:\\output\\"

    
for root, subdirs, files in os.walk(walk_dir):
    for filename in files:
        topic = root.split(os.path.sep)[-2]
        subtopic = root.split(os.path.sep)[-1]
        file_path = os.path.join(root, filename)
        logger.info('extracting: '+file_path)
        with open(file_path, encoding="utf8") as f:
            content = f.readlines()
            start_index = get_startIndex(content)
            end_index = get_endIndex(content)
            tmp_file = []
            for linenum, line in enumerate(content[start_index+1:end_index]):
                tmp_file.append(line)
            new_end_index = remove_extras(tmp_file)
            final_file = []
            for linenum, line in enumerate(tmp_file[0:new_end_index]):
                final_file.append(line)
            logger.info('extraction complete: '+file_path)
            directory = "d:/keypoints/"+topic+"/"+subtopic.lower()
            logger.info('Saving to disk')
            if not os.path.exists(directory):
                logger.info("creating directory "+directory)
                os.makedirs(directory)
            logger.info("writing file: "+directory+"/"+filename)
            with open(directory+"/"+filename+".txt", "w+", encoding="utf-8") as wf:
                wf.writelines(final_file)
            
  
