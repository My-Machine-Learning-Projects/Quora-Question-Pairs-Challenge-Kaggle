# The aim of this program is to generate submission.csv
# Steps:
# 1. Create submission.csv with columns test_id and is_duplicate
# 2. Open test_final.csv (basically test.csv without the first header row and last few empty rows)
# 3. Calculate cosine and wordnet similarity (and then combined/average similarity) for each question pair
# 4. Write the combined_similarity value to the is_duplicate column of submission.csv
# (This is done because the contest states that submission.csv must contain probability scores (between 0 and 1)
# instead of 0 and 1 for the is_duplicate column)
# 5. Also write test_id to submission.csv
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
# functions for WordNet Similarity (i.e. sentence similarity using WordNet)


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified WordNet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    """ Return synsets """
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def sentence_similarity(sentence1, sentence2):
    """ Compute the sentence similarity using WordNet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar synset in the other sentence
        similarity_scores_of_synsets_in_synsets2 = [synset.path_similarity(ss) for ss in synsets2]
        if similarity_scores_of_synsets_in_synsets2:  # check if similarity_scores_of_synsets_in_synsets2 is not empty
            best_score = max(similarity_scores_of_synsets_in_synsets2)
        else:
            best_score = 0

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # Average the values
    if count != 0:
        score /= count
    else:
        score = 0
    return score


def symmetric_sentence_similarity(sentence1, sentence2):
    """ Compute the symmetric sentence similarity using WordNet """
    return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2

########################################################################################################################
# getting combined similarity values for rows in test_final.csv
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

            # change encoding to utf-8 for calculating wordnet similarity
            text1 = text1.encode('utf-8').strip()
            text2 = text2.encode('utf-8').strip()

            # get cosine similarity
            cosine = get_cosine(vector1, vector2)

            # get wordnet similarity (exceptions, if any, arise at this instruction)
            wordnet = symmetric_sentence_similarity(text1, text2)

            # get combined (average) similarity
            combined_similarity = (cosine + wordnet) / 2

            # filling data list
            data.append([int(line[1][0]), float(combined_similarity)])  # line[1][0] has test_id value

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
with open('submission.csv', 'wb') as myfile:
    writer = csv.DictWriter(myfile, fieldnames=["test_id", "is_duplicate"])
    writer.writeheader()
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(data)
