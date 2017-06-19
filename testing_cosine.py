# This program aims to check if cosine similarity is a good metric to estimate the similarity between two sentences
# It uses train_similar_not_similar_combined.csv, which is basically an updated version of train.csv formed
# after removing the UnicodeDecodeError-causing characters in train_not_similar.csv
# and then combining train_similar.csv and train_not_similar.csv using MATLAB

# It makes use of the cosine similarity threshold calculated before i.e. 0.503618.
# If the cosine similarity value <= threshold, predicted_label = 0. Otherwise, predicted_label = 1
# Then, compare actual and predicted labels to get accuracy.

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

predicted_labels = []
actual_labels = []
# open the csv file
with open("train_similar_not_similar_combined.csv", "rb") as f1:
    reader1 = csv.reader(f1, delimiter=",")
    for line in enumerate(reader1):
        text1 = line[1][0]  # first question
        text2 = line[1][1]  # second question

        # print line[1][0]
        # print line[1][1]
        # print line[1][2]

        # convert to vectors
        vector1 = text_to_vector(text1)
        vector2 = text_to_vector(text2)

        # get cosine similarity
        cosine = get_cosine(vector1, vector2)

        # append actual label to actual_labels
        actual_labels.append(int(line[1][2]))

        cosine_similarity_threshold = 0.503618
        if cosine <= cosine_similarity_threshold:
            predicted_label = 0
        else:
            predicted_label = 1
        predicted_labels.append(predicted_label)

# getting accuracy by comparing actual_labels with predicted_labels
matches_count = 0
for i in range(len(actual_labels)):
    if actual_labels[i] == predicted_labels[i]:
        matches_count += 1

accuracy = (matches_count/float(len(actual_labels)))*100
print "Accuracy obtained using Cosine Similarity as a metric: %f %%" % accuracy
print "There were %d matches out of %d rows." % (matches_count, len(actual_labels))
