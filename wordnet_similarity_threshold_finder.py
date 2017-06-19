# first install nltk using cmd, start the python 2.7.10 interpreter, import nltk, and execute nltk.download():
# pip install nltk
# python
# >>> import nltk
# >>> nltk.download()

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
 
    
total_wordnet_similar = 0  # sum of wordnet similarity values for all similar question pairs
total_wordnet_not_similar = 0  # sum of wordnet similarity values for all not-similar question pairs

similar_count = 0  # number of similar question pairs i.e. no of rows in train_similar.csv
not_similar_count = 0  # number of not-similar question pairs i.e. no of rows in train_not_similar.csv

# for getting average value of wordnet similarity for similar question pairs
with codecs.open("train_similar.csv", "rb", encoding='utf-8', errors='ignore') as f1:  # errors = 'ignore' to eliminate the 'unexpected end of data UnicodeDecodeError'
    reader1 = csv.reader(f1, delimiter=",")
    for line in enumerate(reader1):
        text1 = line[1][0]  # first question
        text2 = line[1][1]  # second question

        # change encoding to utf-8
        text1 = text1.encode('utf-8').strip()
        text2 = text2.encode('utf-8').strip()
        
        # get wordnet similarity
        wordnet = symmetric_sentence_similarity(text1, text2)
        
        # add to total value
        total_wordnet_similar += wordnet
        
        # increment count
        similar_count += 1
        print("WS value for similar question pair %d: %f" % (similar_count, wordnet))

average_similar_wordnet = total_wordnet_similar/similar_count  # average value of wordnet similarity for similar question pairs

# for getting average value of wordnet similarity for not-similar question pairs
with codecs.open("train_not_similar.csv", "rb", encoding='utf-8', errors='ignore') as f2:
    reader2 = csv.reader(f2, delimiter=",")
    for line in enumerate(reader2):
        text1 = line[1][0]  # first question
        text2 = line[1][1]  # second question

        # change encoding to utf-8
        text1 = text1.encode('utf-8').strip()
        text2 = text2.encode('utf-8').strip()

        # get wordnet similarity
        wordnet = symmetric_sentence_similarity(text1, text2)

        # add to total value
        total_wordnet_not_similar += wordnet
        
        # increment count
        not_similar_count += 1
        print("WS value for not-similar question pair %d: %f" % (not_similar_count, wordnet))

average_not_similar_wordnet = total_wordnet_not_similar/not_similar_count  # average value of wordnet similarity for not-similar question pairs

# print results
print("\n\nFOR SIMILAR QUESTION PAIRS:")
print("\nTotal similar wordnet similarity : %f" % total_wordnet_similar)
print("Number of similar question pairs : %d" % similar_count)
print("Average similar wordnet similarity : %f" % average_similar_wordnet)

print("\n\nFOR NOT-SIMILAR QUESTION PAIRS:")
print("\nTotal not-similar wordnet similarity : %f" % total_wordnet_not_similar)
print("Number of not-similar question pairs : %d" % not_similar_count)
print("Average not-similar wordnet similarity : %f" % average_not_similar_wordnet)

threshold_for_wordnet_similarity = (average_similar_wordnet + average_not_similar_wordnet) / 2
print("\n\nThreshold for wordnet similarity: %f" % threshold_for_wordnet_similarity)
