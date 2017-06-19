# This program aims to check if wordnet similarity is a good metric to estimate the similarity between two sentences
# It uses train_similar_not_similar_combined.csv, which is basically an updated version of train.csv formed
# after removing the UnicodeDecodeError-causing characters in train_not_similar.csv
# and then combining train_similar.csv and train_not_similar.csv using MATLAB

# It makes use of the wordnet similarity threshold calculated before i.e. 0.698614.
# If the wordnet similarity value <= threshold, predicted_label = 0. Otherwise, predicted_label = 1
# Then, compare actual and predicted labels to get accuracy.

from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
import csv
import codecs
import sys

# changing the encoding to prevent UTF encoding errors
reload(sys)
sys.setdefaultencoding('utf8')


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
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
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None

    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
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
        # Get the similarity value of the most similar word in the other sentence
        # modified to avoid empty argument error
        similarity_scores_of_synsets_in_synsets2 = [synset.path_similarity(ss) for ss in synsets2]
        if similarity_scores_of_synsets_in_synsets2:  # this checks if similarity_scores_of_synsets_in_synsets2 is not empty
            best_score = max(similarity_scores_of_synsets_in_synsets2)
        else:
            best_score = 0

        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1

    # Average the values (modified to avoid divide by zero error)
    if count != 0:
        score /= count
    else:
        score = 0
    return score


def symmetric_sentence_similarity(sentence1, sentence2):
    """ compute the symmetric sentence similarity using Wordnet """
    return (sentence_similarity(sentence1, sentence2) + sentence_similarity(sentence2, sentence1)) / 2

predicted_labels = []
actual_labels = []
# open the csv file
with codecs.open("train_similar_not_similar_combined.csv", "rb", encoding='utf-8',
                 errors='ignore') as f1:  # errors = 'ignore' to eliminate the 'unexpected end of data UnicodeDecodeError'
    reader1 = csv.reader(f1, delimiter=",")
    for line in enumerate(reader1):
        text1 = line[1][0]  # first question
        text2 = line[1][1]  # second question

        # change encoding to utf-8
        text1 = text1.encode('utf-8').strip()
        text2 = text2.encode('utf-8').strip()

        # get wordnet similarity
        wordnet = symmetric_sentence_similarity(text1, text2)

        # append actual label to actual_labels
        actual_labels.append(int(line[1][2]))

        wordnet_similarity_threshold = 0.698614
        if wordnet <= wordnet_similarity_threshold:
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
print "Accuracy obtained using WordNet Similarity as a metric: %f %%" % accuracy
print "There were %d matches out of %d rows." % (matches_count, len(actual_labels))
