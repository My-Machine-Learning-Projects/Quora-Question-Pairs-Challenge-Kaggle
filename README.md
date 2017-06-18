# Quora-Question-Pairs-Challenge-Kaggle
This was my attempt at solving the "Quora Question Pairs" challenge on Kaggle.  
Competition link: https://www.kaggle.com/c/quora-question-pairs  
This was also the first time that I attempted to solve a challenge that involved NLP (Natural Language Processing).  
  
_Although I didn't do so well in the competition (I ranked 2798/3307), I consider this as more of a learning experience._  

## My Process ##
The data for this challenge was made available on the competition website: https://www.kaggle.com/c/quora-question-pairs/data  

### Pre-Processing ##
I downloaded train.csv and test.csv from the above link. Then, I used MATLAB to split train.csv into two files (train_not_similar.csv and train_similar.csv) based on the values in the 'is_duplicate' column i.e. 0 an 1 respectively.  

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
