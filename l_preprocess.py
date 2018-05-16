import re
import preprocess
import os

for root, subdirs, files in os.walk("d:\\keypoints\\"):
    for filename in files:
        topic = root.split(os.path.sep)[-2]
        subtopic = root.split(os.path.sep)[-1]
        file_path = os.path.join(root, filename)
        with open(file_path, encoding="utf8") as f:
            contents = f.readlines()
        ##Converting the texts to lowercase
        contents = preprocess.to_lower(contents)
        ##Converting the texts into tokenized sentences also, removing the stop words
        contents = preprocess.process_sentences(contents)
        ##Stripping punctuations
        preprocessed_file = []
        for line in contents:
            preprocessed_file.append(preprocess.remove_punct(line))
        preprocessed_file = preprocess.remove_numbers(preprocessed_file)
        preprocessed_file = preprocess.normalize_whitespace(preprocessed_file)
        preprocessed_file = preprocess.remove_currency_symbols(preprocessed_file)
        #print(filename)
        directory = "d:\\tmp\\"+topic+"\\"+subtopic.lower()
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory+ '\\'+filename, 'w+', encoding='utf-8') as wf:
            wf.write('\n'.join(preprocessed_file)) 
