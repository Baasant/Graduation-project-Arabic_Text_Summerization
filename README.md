# Graduation-project-Arabic_Text_Summerization
This folder contains best scores for ATS system
1- English summarization notebook contains a generic model where you can input an English text and get its summary
2- DUC2001- Best Results contains EdgeSumm model tested on DUC2001 Dataset, with graph nodes as nouns and verbs and no clustring as it gave us the best results
3- DUC2002- Best Results contains EdgeSumm model tested on DUC2002 Dataset, with graph nodes as nouns and verbs and no clustring as it gave us the best results
4- Arabic summarization notebook contains a generic model where you can input an Arabic text and get its summary
5- Translated_Arabic_to_English is the same as english model but tested on translated Arabic Data using Essex Arabic summaries corpus using textblob translation module

# Code documentation for Automatic Evaluation based on machine learning approach 
We pass 11 feature to our classifiers and make some experiments to  get the best result
Features that we used 
1-MeMoG:we pass to it the candidate summary  and the reference summary  we have 3 references for each candidate through these 3 references generating the merged graph which compared with the candidate graph 
2-Lexical Features:for the candidate summary we pass it to a POS and have a list of Nouns  and verbs then calculate the Number of Nouns and verbs in each candidate summary and after that calculate the density of each type in each  candidate summary  
3-SIMetrix:: we pass to it frequency of each word in candidate summary and in the input source  then calculate the divergence from the input to candidate and the divergence from the candidate to source input and then calculating the smoothed version of it 
5-ROUGE:we pass to it the candidate summary and the reference summary , we have 3 references for each candidate so we take the average of them, and calculate Rouge 1, Rouge 2, Rouge 3 and Rouge 4


# Demo Interview 
Create a demo interview 
as interview questions and based on his/her answer,time that he /she takes to answer
1-Use the sentiment analysis to know the feelings of interviewee such as worry,ego,loyalty
2-Time he/she used to answet the questions 
to evaluate the interviewee
