import csv
import re
import math
from collections import Counter

WORD = re.compile(r'\w+')


def get_cosine(vec1, vec2):
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
    words = WORD.findall(text)
    return Counter(words)

total_cosine_similar = 0  # sum of cosine similarity values for all similar question pairs
total_cosine_not_similar = 0  # sum of cosine similarity values for all not-similar question pairs

similar_count = 0  # number of similar question pairs i.e. no of rows in train_similar.csv
not_similar_count = 0  # number of not-similar question pairs i.e. no of rows in train_not_similar.csv

# for getting average value of cosine similarity for similar question pairs
with open("train_similar.csv", "rb") as f1:
    reader1 = csv.reader(f1, delimiter=",")
    for line in enumerate(reader1):
        text1 = line[1][0]  # first question
        text2 = line[1][1]  # second question

        # convert to vectors
        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        # get cosine similarity
        cosine = get_cosine(vector1, vector2)

        # add to total value
        total_cosine_similar += cosine

        # increment count
        similar_count += 1
        #print "CS value for similar question pair %d: %f"%(similar_count, cosine)

average_similar_cosine = total_cosine_similar/similar_count  # average value of cosine similarity for similar question pairs

print "\n\nFOR SIMILAR QUESTION PAIRS:"
print "\nTotal similar cosine similarity : %f" % total_cosine_similar
print "Number of similar question pairs : %d" % similar_count
print "Average similar cosine similarity : %f" % average_similar_cosine

# for getting average value of cosine similarity for not-similar question pairs
with open("train_not_similar.csv", "rb") as f2:
    reader2 = csv.reader(f2, delimiter=",")
    for line in enumerate(reader2):
        text1 = line[1][0]  # first question
        text2 = line[1][1]  # second question

        # convert to vectors
        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        # get cosine similarity
        cosine = get_cosine(vector1, vector2)

        # add to total value
        total_cosine_not_similar += cosine

        # increment count
        not_similar_count += 1
        #print "CS value for similar question pair %d: %f"%(not_similar_count, cosine)

average_not_similar_cosine = total_cosine_not_similar/not_similar_count  # average value of cosine similarity for not-similar question pairs

print "\n\nFOR NOT-SIMILAR QUESTION PAIRS:"
print "\nTotal not-similar cosine similarity : %f" % total_cosine_not_similar
print "Number of not-similar question pairs : %d" % not_similar_count
print "Average not-similar cosine similarity : %f" % average_not_similar_cosine

threshold_for_cosine_similarity = (average_similar_cosine + average_not_similar_cosine) / 2
print "\n\nThreshold for cosine similarity: %f" % threshold_for_cosine_similarity
