#!/usr/bin/python
#Extract title, abstract, keywords, introduction and conclusions
import os
import re

## Call this method when conclusion is not found in greedy approach
##Iterates the content in reverse and returns the conclusion and conclusion_ values
def find_conclusion(contents):
    references = 'REFERENCES'
    bibliography = 'BIBLIOGRAPHY'
    acknowledgements = 'ACKNOWLEDGEMENTS'
    regex_reference = re.compile(r"\bREFERENCES|BIBLIOGRAPHY|ACKNOWLEDGEMENTS\b", re.IGNORECASE)
    conclusion = conclusion_ = 0
    for linenum, line in enumerate(reversed(contents)):
        if conclusion_ != 0:
            if re.match(r"(\d|(IX|IV|V?I{0,3}))\.\s+\w.*", line) != None and references not in line.capitalize() or bibliography not in line.capitalize() or acknowledgements not in line.capitalize():
                conclusion = len(contents) -1 -linenum
                break
        else:
            if re.match(r"(\d|(IX|IV|V?I{0,3}))\.\s+\w.*", line) != None:
                conclusion_ = len(contents) -1 -linenum
                continue
            elif regex_reference.search(line) != None:
                conclusion_ = len(contents) -1 -linenum
                continue
    
    return conclusion, conclusion_

def get_boundaries(contents):
    ##Find the boundaries using simple pattern matchings
    def pattern_lookup(contents):
        ##Variables with _ denotes the ending index for that context
        abstract = introduction = introduction_ = conclusion = conclusion_ = 0;
        ##regex for the boundaries
        regex_abstract = re.compile(r"\bABSTRACT\b", re.IGNORECASE)
        regex_introduciton = re.compile(r"(\d|(IX|IV|V?I{0,3}))\.\s+\INTRODUCTION", re.IGNORECASE)
        regex_conclusion = re.compile(r"(\d|(IX|IV|V?I{0,3}))\.\s+(\w.*CONCLUSION|\CONCLUSION|\SUMMARY)", re.IGNORECASE)
        regex_reference = re.compile(r"\bREFERENCES|BIBLIOGRAPHY|ACKNOWLEDGEMENTS\b", re.IGNORECASE)
        
        for linenum, line in enumerate(contents):
            if abstract == 0 and regex_abstract.search(line) != None:
                abstract = linenum
                continue
            elif introduction == 0 and regex_introduciton.search(line) != None:
                introduction = linenum
                continue
            ##Get the index of the next starting pattern to find the ending of current pattern.    
            if introduction != 0:
                if re.match(r"(\d|(IX|IV|V?I{0,3}))\.\s+\w.*", line) != None and introduction_ == 0:
                    introduction_ = linenum
                    continue
                elif introduction_ != 0 and conclusion == 0:
                    if regex_conclusion.search(line) != None :
                        conclusion = linenum
                        continue
                elif conclusion != 0 and conclusion_ == 0:
                    if re.match(r"(\d|(IX|IV|V?I{0,3}))\.\s+\w.*", line) != None:
                        conclusion_ = linenum
                        break
                    elif regex_reference.search(line) != None:
                        conclusion_ = linenum
                        break
                    
        return abstract, introduction, introduction_, conclusion, conclusion_
    
    ##Find the boundaries using greedy pattern selections
    def greedy_pattern_lookup(contents):
        ##Look in basic patterns first
        abstract, introduction, introduction_, conclusion, conclusion_ = pattern_lookup(contents)
        
        regex_greedy_introduction = re.compile(r"\bINTRODUCTION\b", re.IGNORECASE)
        regex_conclusion = re.compile(r"\bSUMMARY|CONCLUSION(|S)\b", re.IGNORECASE)        
#        regex_greedy_conclusion = re.compile(r"\bLessons (L|l)earned\b")
        regex_reference = re.compile(r"\bREFERENCES|BIBLIOGRAPHY|ACKNOWLEDGEMENTS\b", re.IGNORECASE)
        
        if(introduction == 0 and introduction_ == 0):
            for linenum, line in enumerate(contents):
                if (introduction == 0):
                    if regex_greedy_introduction.search(line) != None and len(line) <20 and 'I' in line:
                        introduction = linenum
                        continue
                elif (introduction != 0 and introduction_ == 0):
                    if re.match(r"(\d|(IX|IV|V?I{0,3}))\.\s+\w.*", line) != None:
                        introduction_ = linenum
                        break
            if(introduction != 0 and introduction_ == 0):
                for linenum, line in enumerate(contents[introduction:]):
                    if re.match(r"[A-Z][a-zA-Z\\s]*", line) != None and len(line.split()) < 3 and '\n' in line:
                        ## A naive approach to get the next heading
                        introduction_ = linenum + introduction
                        break
        
        ##Finding conclusion using greedy patterns
        if(introduction != 0 and introduction_ != 0 and conclusion == 0 and conclusion_ == 0):
            for linenum, line in enumerate(contents[introduction_:]):
                if regex_conclusion.search(line) != None and ('C' in line or 'S' in line):
                    conclusion = linenum + introduction_
                    continue
#                elif regex_greedy_conclusion.search(line) != None:
#                    conclusion = linenum + introduction_
#                    continue
                elif conclusion != 0 and conclusion_ == 0:
                    ##Get the index of the next starting pattern to find the ending of current pattern.
                    if re.match(r"(\d|(IX|IV|V?I{0,3}))\.\s+\w.*", line) != None:
                        conclusion_ = linenum + introduction_
                        break
                    elif regex_reference.search(line) != None:
                        conclusion_ = linenum + introduction_
                        break
#            if(conclusion == 0 and conclusion_ == 0):
#                conclusion, conclusion_ = find_conclusion(contents)
                        
        return abstract, introduction, introduction_, conclusion, conclusion_
    
    abstract, introduction, introduction_, conclusion, conclusion_ = greedy_pattern_lookup(contents)

    return abstract, introduction, introduction_, conclusion, conclusion_
    
##extracts information from the text files.
def feature_extraction(walk_dir, output_dir):
    for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            with open(file_path, encoding="utf8") as f:
                contents = f.readlines()
            contents = format_contents(contents)
            abstract, introduction, introduction_, conclusion, conclusion_ = get_boundaries(contents)
            if (introduction != 0 and introduction != 0 and conclusion != 0 and conclusion_ != 0):
                with open(output_dir+filename, "w+", encoding="utf-8") as wf:
                    if(abstract != 0):
                        ##Some pdf's dont contain an abstract so we omit it
                        wf.writelines(contents[abstract:introduction])
                
                    wf.writelines(contents[introduction:introduction_])
                    wf.writelines(contents[conclusion:conclusion_])
