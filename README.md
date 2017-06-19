# Quora-Question-Pairs-Challenge-Kaggle
This was my attempt at solving the "Quora Question Pairs" challenge on Kaggle.  
Competition link: https://www.kaggle.com/c/quora-question-pairs  
This was also the first time that I attempted to solve a challenge that involved NLP (Natural Language Processing).  
  
_Although I didn't do so well in the competition (I ranked 2798/3307), I consider this as more of a learning experience._  

## My Process ##
The data for this challenge was made available on the competition website: https://www.kaggle.com/c/quora-question-pairs/data  

### Pre-Processing ##
I downloaded train.csv and test.csv from the above link. Then, I used MATLAB to split train.csv into two files (train_not_similar.csv and train_similar.csv) based on the values in the 'is_duplicate' column i.e. 0 and 1 respectively.  

To do so, in MATLAB, I first loaded train.csv (as a table) by doube-clicking on it, and then executed the following commands in the command window:

```train = train(:, 4:end);  % removes first 3 columns  
train = train(1:404290, :);  % to remove empty rows at the end  
  
% splitting into train_similar.csv and train_not_similar.csv  
last_column = train(:, end);  
last_column = table2array(last_column);  
similar = train(last_column==1, :);  
not_similar = train(last_column==0, :);  
writetable(similar, 'train_similar.csv');  
writetable(not_similar, 'train_not_similar.csv');
```    

This created train_similar.csv and train_not_similar.csv.  
  
I used Python for the rest of the process. However, since Python reads csv files from first line and takes the header as the first line, I removed the first row (header row i.e. question1, question2, is_duplicate) from both the files using LibreOffice Calc.  

### Processing ### 
I tried 3 different approaches:
1. Using Cosine Similarity as a metric
2. Using WordNet Similarity as a metric
3. Using both together (Combined Similarity) as a metric

_NOTE: Before calculating accuracy, I created train_similar_not_similar_combined.csv using MATLAB._  
  
These steps were used to get train_similar_not_similar_combined.csv:

1. Open MATLAB.
2. Load both the csv files (train_similar.csv and train_not_similar.csv) as tables, by double clicking on them. Make sure to change the column headers to question1, question2 and is_duplicate before importing.
They get imported as workspace variables trainsimilar and trainnotsimilar.
3. Type the following in the command window:

```a = trainsimilar;
b = trainnotsimilar;
c = vertcat(a,b);
trainsimilarnotsimilarcombined = c;
trainsimilarnotsimilarcombined = trainsimilarnotsimilarcombined(1:404290, :); % to remove some empty rows at the end
writetable(trainsimilarnotsimilarcombined, 'train_similar_not_similar_combined.csv');
```

However, the first row of train_similar_not_similar_combined.csv becomes "question1, question2, is_duplicate". So, remove that row using LibreOffice Calc.

#### 1. Using Cosine Similarity as a metric ####
**cosine_similarity_threshold_finder.py** determines the average threshold cosine similarity value for similar/notsimilar question pairs. It does so by first calculating the cosine similarity for each question pair and taking the corresponding averages. Refer the program for detailed explanation (explained in the comments).  
  
The following is the output of the program:  
![Output of cosine_similarity_threshold_finder.py](https://github.com/My-Machine-Learning-Projects/Quora-Question-Pairs-Challenge-Kaggle/blob/master/Threshold%20for%20Cosine%20Similarity%20value.PNG "Output of cosine_similarity_threshold_finder.py")

##### Accuracy #####
The accuracy was calculated using **testing_cosine.py**. See the program for explanation.  
  
The following accuracy was obtained using Cosine Similarity as a metric:
![Output of testing_cosine.py](https://github.com/My-Machine-Learning-Projects/Quora-Question-Pairs-Challenge-Kaggle/blob/master/Accuracy%20using%20Cosine%20Similarity.PNG "Output of testing_cosine.py")

#### 2. Using WordNet Similarity as a metric ####
WordNet similarity is basically the similarity between 2 sentences, calculated using WordNet. So, this is a better measure than cosine similarity because it incorporates semantic similarity. It internally looks for synsets for each word in the sentence and compares them to those of the words in the other sentence. However, it took much longer to compute.  
  
**wordnet_similarity_threshold_finder.py** determines the average threshold wordnet similarity value for similar/notsimilar question pairs. It does so by first calculating the wordnet similarity for each question pair and taking the corresponding averages. Refer the program for detailed explanation (explained in the comments).  
  
_NOTE: There was a UTF-8 encoding issue while running the program. Changes have been made in the program to avoid those errors._
  
The following is the output of the program:  
![Output of wordnet_similarity_threshold_finder.py](https://github.com/My-Machine-Learning-Projects/Quora-Question-Pairs-Challenge-Kaggle/blob/master/Threshold%20for%20Wordnet%20Similarity%20value.PNG "Output of wordnet_similarity_threshold_finder.py")

##### Accuracy #####
The accuracy was calculated using **testing_wordnet.py**. See the program for explanation.  
  
The following accuracy was obtained using WordNet Similarity as a metric:
![Output of testing_wordnet.py](https://github.com/My-Machine-Learning-Projects/Quora-Question-Pairs-Challenge-Kaggle/blob/master/Accuracy%20using%20WordNet%20Similarity.PNG "Output of testing_wordnet.py")

As shown, it achieved a lower accuracy than testing_cosine.py.  

#### 2. Using both together (Combined Similarity) as a metric ####
The combined threshold is the average of the Cosine Similarity threshold and the WordNet Similarity threshold.  

##### Accuracy #####
The accuracy was calculated using **testing_combined.py**. See the program for explanation.  
  
The following accuracy was obtained using Combined Similarity as a metric:
![Output of testing_combined.py](https://github.com/My-Machine-Learning-Projects/Quora-Question-Pairs-Challenge-Kaggle/blob/master/Accuracy%20using%20Combined%20Similarity.PNG "Output of testing_combined.py")

As shown, it achieved a slightly higher accuracy than testing_cosine.py.

### My Submissions ###

#### Some Preprocessing ####
The test.csv file has a few empty rows at the bottom. To remove them, I used MATLAB.  
In MATLAB, I loaded test.csv as a table by double-clicking on it. It gets loaded as a workspace variable called 'test'. To remove the last few empty rows, I executed the following in the command window:  
```testfinal = test;
testfinal = testfinal(1:2345796, :);  % remove empty rows
writetable(testfinal, 'test_final.csv');  % save as test_final.csv
```
This creates test_final.csv.  
Now, since Python will treat the header row as the first line, I removed the first row (test_id, question1, question2) from test_final.csv using a software called CSVEd. (LibreOffice Calc wasn't able to open the file and threw this error: "The maximum number of rows has been exceeded."). That's why I had to use CSVEd.

#### Submission Attempts ####
I had two submissions, one using Cosine Similarity and the other using Combined Similarity. Log loss was used as the testing metric by Kaggle.  
The two submissions were as follows:
##### 1. Using Cosine Similarity #####
This submission made use of Cosine Similarity to estimate the similarity between two sentences/questions.  
Check **test_cosine.py** for explanation. It calculates the Cosine Similarity between the question pairs in test_final.csv and creates submission_cosine.csv, which I submitted on Kaggle. This submission received a Log Loss score of 0.71878, and ranked 2798/3307 on the final leaderboard.

##### 2. Using Combined Similarity #####
This submission made use of Combined Similarity (a combination of Cosine Similarity and WordNet Similarity) to estimate the similarity between two sentences/questions.  
Check **test.py** for explanation. It calculates the Combined Similarity between the question pairs in test_final.csv and creates submission.csv, which I submitted on Kaggle. This submission received a Log Loss score of 0.82967. A higher Log Loss score indicates lower accuracy, therefore it wasn't an improvement over my first submission.  
  
Therefore, my first submission was considered as my final submission.  
  
Although I didn't perform well enough in the competition, I decided to share my experience here anyway.  
