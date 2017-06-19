# The aim of this program is to generate submission_cosine.csv
# Steps:
# 1. Create submission_cosine.csv with columns test_id and is_duplicate
# 2. Open test_final.csv (basically test.csv without the first header row and last few empty rows)
# 3. Calculate cosine similarity for each question pair
# 4. Write the cosine similarity value to the is_duplicate column of submission_cosine.csv
# (This is done because the contest states that submission.csv must contain probability scores (between 0 and 1)
# instead of 0 and 1 for the is_duplicate column)
# 5. Also write test_id to submission_cosine.csv
# The main part of the code is in a try block, and there is an accompanying generic catch block to catch any exception
# and let the program keep running even if an exception occurs. It will print the row number at which exception occurs.

import csv
import re
import math
from collections import Counter
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import codecs
import sys
# changing the encoding to prevent UTF encoding errors
reload(sys)
sys.setdefaultencoding('utf8')

WORD = re.compile(r'\w+')

########################################################################################################################
# functions for Cosine Similarity


def get_cosine(vec1, vec2):
    """ Return cosine similarity value between vec1 and vec2 """
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    """ Vectorize a sentence """
    words = WORD.findall(text)
    return Counter(words)


########################################################################################################################
# getting cosine similarity values for rows in test_final.csv
row_num = 0
exception_rows = []  # test_id rows (row_num - 1) at which an exception occurred
data = []  # a list that will be used while filling submissions.csv
# open test_final.csv
with codecs.open("test_final.csv", "rb", encoding='utf-8', errors='ignore') as f1:
    reader1 = csv.reader(f1, delimiter=",")
    for line in enumerate(reader1):
        try:  # to allow the program to continue running even if an exception occurs
            # increment row count
            row_num = row_num + 1
            
            text1 = line[1][1]  # first question
            text2 = line[1][2]  # second question
            
            # convert to vectors for calculating cosine similarity
            vector1 = text_to_vector(text1)
            vector2 = text_to_vector(text2)
            
            # get cosine similarity
            cosine = get_cosine(vector1, vector2)
            
            # filling data list
            data.append([int(line[1][0]), float(cosine)])  # line[1][0] has test_id value
            
            # print percentage completion
            per = (row_num / float(2345796.0)) * 100
            print "Percentage of completion (approx.): %f %%" % per
        except Exception:
            exception_rows.append(row_num - 1)
            # assign neutral similarity (0.5) for the row that caused the exception
            data.append([int(line[1][0]), float(0.5)])

if exception_rows:  # check if exception_rows isn't empty 
    print "Exceptions occurred at the following rows (test_ids) of test_final.csv:"
    print exception_rows

# fill submissions.csv with data list
with open('submission_cosine.csv', 'wb') as myfile:
    writer = csv.DictWriter(myfile, fieldnames=["test_id", "is_duplicate"])
    writer.writeheader()
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(data)
