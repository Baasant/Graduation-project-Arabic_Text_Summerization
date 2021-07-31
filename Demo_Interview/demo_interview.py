#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os 
import time 
import playsound
import re
import random
import speech_recognition as sr
from gtts import gTTS as sp
import rouge_score
from rouge_score import rouge_scorer
from difflib import SequenceMatcher 
from rouge_score import rouge_scorer
from nltk import pos_tag
import nltk
nltk.download('averaged_perceptron_tagger')
import language_tool_python
tool_en = language_tool_python.LanguageTool('en-US')
tool_ar = language_tool_python.LanguageTool('ar-EG')
from tkinter import messagebox
from tkinter import *
from tkinter import ttk


# In[2]:


# class is to record all infromation about the interview 
class interview:
    
    
    def __init__(self,interview_name):
        self.name=interview_name
        self.interview_questions=[]
        self.interview_interviewer_answer={}
        self.interview_model_question_answers={}
        self.question_bad_answer={}
        self.feedback={}
        self.time_limit={}
        self.feedback_ev={}
        self.question_Score_ev={}
        self.grammar_miss_corr_ev={}
        self.grammar_score_ev={}
        self.rouge_score_ev={}
        self.time_score_ev={}
        self.worry_score_ev={}
        self.greedy_score_ev={}
        self.ambitious_score_ev={}
        self.vanity_score_ev={}
        self.loyalty_score_ev={}
        self.q_weight={}
        self.q_weight[0.05]=[]
        self.q_weight[0.1]=[]
        self.q_weight[0.15]=[]
        self.q_weight[0.20]=[]
        self.q_weight[0.25]=[]
        self.q_weight[0.30]=[]
        self.q_weight[0.35]=[]
        self.q_weight[0.40]=[]
        self.q_weight[0.45]=[]
        self.q_weight[0.50]=[]
        self.q_weight[0.55]=[]
    
    def add_question_and_model_answer(self,question,good_answer,bad_answer,feedbacks,time_limits,qe_weight):
        self.interview_questions.append(question)
        self.interview_model_question_answers[question]=good_answer
        self.feedback[question]=feedbacks
        self.time_limit[question]=time_limits
        self.question_bad_answer[question]=bad_answer
        self.q_weight[qe_weight].append(question)
        
        
    def get_question(self,weightx):
        questionw=""
        try:
            questionw=random.choice(self.q_weight[weightx])
            self.q_weight[weightx].remove(questionw)
        except:
            print("error in interview class")
        return questionw
    
    
    def add_interviewer_answer(self,question,answer):
        self.interview_interviewer_answer[question]=answer
        
    
    def list_of_questions(self):
        return self.interview_questions
    
    
    def return_feedback(self,question):
        return self.feedback[question]
    
    
    #use it for plagiarism check and how good is the interviewer answer 
    def dict_of_questions_and_model_answers(self):
        return self.interview_model_question_answers
    
    
    def question_time_limits(self,question):
        return self.time_limit[question]
        
        
    def question_and_bad_answer(self,question):
        return self.question_bad_answer[question]
    
    
    def return_interviewer_answer(self,question):
        return self.interview_interviewer_answer[question]
        
    
    #evaluation_of_question_list=
    def evaluation_add(self,question,question_score,mistake_correction,feedback_to_answer,wor_score,amb_score,greed_score,loy_score,van_score,rog_score,gr_score,ti_score):
        self.feedback_ev[question]=feedback_to_answer
        self.question_Score_ev[question]=question_score
        self.grammar_miss_corr_ev[question]=mistake_correction
        self.grammar_score_ev[question]=gr_score
        self.rouge_score_ev[question]=rog_score
        self.time_score_ev[question]=ti_score
        self.worry_score_ev[question]=wor_score
        self.greedy_score_ev[question]=greed_score
        self.ambitious_score_ev[question]=amb_score
        self.vanity_score_ev[question]=van_score
        self.loyalty_score_ev[question]=loy_score
            
        
        
    


# In[3]:


#preprocessing
def normalizestring(s):
    s=s.lower().strip()
    s=re.sub(r"([.?!])",r" \1",s)
    s=re.sub(r"'m",r" am",s)
    s=re.sub(r"'s",r" is",s)
    #s=re.sub(r"he's",r"he is",s)
    #s=re.sub(r"she's",r"she is",s)
    s=re.sub(r"'re",r" are",s)
    s=re.sub(r"'ll",r" will",s)
    #s=re.sub(r"we're",r"we are",s)
    #s=re.sub(r"[^a-zA-Z.?!]+",r" ",s)
    s=re.sub(r"[^a-zA-Z0-9]+",r" ",s)
    s=re.sub(r"\s+",r" ",s).strip()  
    return s

#preprocessing
def normalizestringlist(l):
    new_list=[]
    for s in l:
        s=s.lower().strip()
        s=re.sub(r"([.?!])",r" \1",s)
        s=re.sub(r"'m",r" am",s)
        s=re.sub(r"'s",r" is",s)
        #s=re.sub(r"he's",r"he is",s)
        #s=re.sub(r"she's",r"she is",s)
        s=re.sub(r"'re",r" are",s)
        s=re.sub(r"'ll",r" will",s)
        #s=re.sub(r"we're",r"we are",s)
        #s=re.sub(r"[^a-zA-Z.?!]+",r" ",s)
        s=re.sub(r"[^a-zA-Z0-9.?!]+",r" ",s)
        s=re.sub(r"\s+",r" ",s).strip() 
        new_list.append(s)
    return new_list
# the data in the textfile are the question followed by the inputs below and separated with % 
# the return of load question data set funtion is the follwing 
#1-questions_expected
#2-question_and_sample_answer
#3-question_and_how_to_answer
#4-question_and_question_weight
#5-question_and_worry_mental_state_weight,
#6-question_and_ambitious_mental_state_weight
#7-question_and_greedy_mental_state_weight
#8-question_and_loyalty_mental_state_weight
#9-question_and_vanity_mental_state_weight
#10-question_and_rouge_score_weight
#11-question_and_good_sample_answers
#12-question_and_bad_answers
#13-question time limit
def load_question_dataset():
    #questions and thier answer and thier feed back 
    question_and_sample_answer={}
    question_and_how_to_answer={}
    question_and_question_weight={}
    question_and_worry_mental_state_weight={}
    question_and_ambitious_mental_state_weight={}
    question_and_greedy_mental_state_weight={}
    question_and_loyalty_mental_state_weight={}
    question_and_vanity_mental_state_weight={}
    question_and_rouge_score_weight={}
    question_and_time_limit={}
    questions_expected=[]
    # hr for refresh will have 9 % marke between 10 different inputs
    # 1- question qa[0]
    # 2- sample answer for the interviewee at the end of the interview qa[1]
    # 3- teach the interviewee how to answer each question proberly qa[2]
    # 4- question weight qa[3]
    # 5- worry mental state weight qa[4]
    # 6- Ambitious mental state weight qa[5]
    # 7- greedy mental state weight qa[6]
    # 8- loyalty mental state weight qa[7]
    # 9- vanity mental state weight qa[8]
    # 10- rouge score weight qa[9]
    # 11- question time limit qa[10]
    with open ("hr for refresh.txt","r",encoding='utf8') as f:
        text_lines=f.readlines()
        for line in text_lines:
            qa=line.split("%")
            questions_expected.append(normalizestring(qa[0]))
            question_and_sample_answer[normalizestring(qa[0])]=normalizestring(qa[1])
            question_and_how_to_answer[normalizestring(qa[0])]=normalizestring(qa[2])
            question_and_question_weight[normalizestring(qa[0])]=float(qa[3])
            question_and_worry_mental_state_weight[normalizestring(qa[0])]=float(qa[4])
            question_and_ambitious_mental_state_weight[normalizestring(qa[0])]=float(qa[5])
            question_and_greedy_mental_state_weight[normalizestring(qa[0])]=float(qa[6])
            question_and_loyalty_mental_state_weight[normalizestring(qa[0])]=float(qa[7])
            question_and_vanity_mental_state_weight[normalizestring(qa[0])]=float(qa[8])
            question_and_rouge_score_weight[normalizestring(qa[0])]=float(qa[9])
            question_and_time_limit[normalizestring(qa[0])]=float(qa[10])
        f.close()

    #bad answers 
    question_and_bad_answers={}
    questions_expected_b=[]
    
    with open ("bad answers.txt","r",encoding='utf8') as f:
        text_lines=f.readlines()
        for line in text_lines:
            qa=line.split("%")
            questions_expected_b.append(normalizestring(qa[0]))
            bad_answer_list=[]
            for i in range(1,len(qa)):
                bad_answer_list.append(qa[i]) 
            question_and_bad_answers[normalizestring(qa[0])]=normalizestringlist(bad_answer_list)
        f.close()

    #check for paraglism and rouge score
    question_and_good_sample_answers={}
    questions_expected_g=[]
    
    with open ("answers for paraglism.txt","r",encoding='utf8') as f:
        text_lines=f.readlines()
        for line in text_lines:
            qa=line.split("%")
            questions_expected_g.append(normalizestring(qa[0]))
            good_answer_list=[]
            for i in range(1,len(qa)):
                good_answer_list.append(qa[i])
            question_and_good_sample_answers[normalizestring(qa[0])]=normalizestringlist(good_answer_list)
        f.close()
    
    return questions_expected,question_and_sample_answer,question_and_how_to_answer,question_and_question_weight,question_and_worry_mental_state_weight,question_and_ambitious_mental_state_weight,question_and_greedy_mental_state_weight,question_and_loyalty_mental_state_weight,question_and_vanity_mental_state_weight,question_and_rouge_score_weight,question_and_good_sample_answers,question_and_bad_answers,question_and_time_limit


# In[4]:


#function vocalize arabic language question
def speak_text_arabic(Text,file_name):
    #transform text to an audio file 
    tts=sp(text=Text,lang="ar")
    filename=file_name+".mp3"
    #save the mp3 file in the folder of the .py file 
    try:
        tts.save(filename)
    except Exception as e:
        filename=filename
    playsound.playsound(filename)
    return True

#function vocalize english language question
def speak_text_english(Text,file_name):
    #transform text to an audio file 
    tts=sp(text=Text,lang="en")
    filename=file_name +".mp3"
    #save the mp3 file in the folder of the .py file 
    try:
        tts.save(filename)
    except Exception as e:
        filename=filename
    playsound.playsound(filename)
    return True 


#record the interveiwee answer and 
def get_audio_english(question_time_limit=60):
    r=sr.Recognizer()
    #r.energy_threshold = 70 #for silent rooms from 0:100 
    #r.energy_threshold = 2000 # from 150 to 3500 is the original 
    #r.energy_threshold = 5000 # in loud rooms 
    #If you're having trouble with the recognizer trying to recognize words even when you're not speaking try higher values 
    # If you're having trouble with the recognizer not recognizing your words when you are speaking, try tweaking this to a lower value
    with sr.Microphone() as source:
        said=""
        try:
            r.adjust_for_ambient_noise(source,duration=0.5)
            audio=r.record(source=source, duration=question_time_limit)
            #audio=r.listen(source,timeout=10.0,phrase_time_limit=float(question_time_limit))
        except Exception as e:
            print ("Exception: " + str(e))
        try:
            said=r.recognize_google(audio)
        except Exception as e:
            print ("Exception: " + str(e))
    
    
    return said


 
    
def get_audio_arabic(question_time_limit=60):
    r=sr.Recognizer()
    with sr.Microphone() as source:
        said=""
        try:
            r.adjust_for_ambient_noise(source,duration=0.5)
            audio=r.record(source=source, duration=20)
            #audio=r.listen(source,timeout=10.0,phrase_time_limit=float(question_time_limit))
        except Exception as e:
            print ("Exception: " + str(e))
        try:
            said=r.recognize_google(audio,language="ar-EG")
            #print(said)
        except Exception as e:
            print ("Exception: " + str(e))
            
    return said    




def get_the_answer_from_the_user_english(question_time_limit,number_of_wrong_recognition):
    # it will take the question time limit estimated for each question 
    #returns the answer for a specific question either by voice or text and returns 2 parameters
    #first is the answer 
    #second is the voice if voice=1 then the evaluation by time and the number of words 
    #if voice =0 then the evaluation is by time spend which is bigger than voice and grammatic and spelling mistakes
    text=""
    if number_of_wrong_recognition < 2:
        text_words=get_audio_english(question_time_limit)
        text=text_words
        print("your Answer: ")
        print(text)
        time_x=time.time()
        ans=input("if this what you have said write 'yes' if it wasn't what you have said please write your answer :  \n")
        if ans =="yes":
            number_of_wrong_recognition=max(number_of_wrong_recognition-1,0)
            answer=text
            text_length=len(text.split())
            if text_length < (question_time_limit/5):
                ev_score=0.01
            elif text_length < (question_time_limit/4):
                ev_score=0.02
            elif text_length < (question_time_limit/3):
                ev_score=0.03
            elif text_length < (question_time_limit/2):
                ev_score=0.04
            else:
                ev_score=0.05
        else:
            
            answer=ans
            number_of_wrong_recognition=number_of_wrong_recognition+1
            time_y=time.time()-time_x
            if time_y<5:
                ev_score=0
            elif time_y > 2*question_time_limit:
                ev_score=0.025
            else:
                ev_score=0.05
            roug_s=rouge_scores_ev(answer,text,"recall")
            if roug_s < 0.5:
                ev_score=max(ev_score-0.05,0.01)
    
    else:
        time_x=time.time()
        answer=input("Please enter your answer ")
        time_y=time.time()-time_x
        if time_y < 5:
            ev_score=0
        elif time_y > 2*question_time_limit:
            ev_score=0.025
        else:
            ev_score=0.05
        roug_s=rouge_scores_ev(answer,text,"recall")
        if roug_s < 0.5:
            ev_score=max(ev_score-0.05,0.01)
    return answer,ev_score,number_of_wrong_recognition



def get_the_answer_from_the_user_arabic(question_time_limit=60):
    # it will take the question time limit estimated for each question 
    #returns the answer for a specific question either by voice or text and returns 2 parameters
    #first is the answer 
    #second is the voice if voice=1 then the evaluation by time and the number of words 
    #if voice =0 then the evaluation is by time spend which is bigger than voice and grammatic and spelling mistakes
    text=""
    text_words=get_audio_arabic(question_time_limit)
    text=text_words
    voice=1
    print("اجابتك: ")
    print(text)
    ans=input("لو كانت هذه اجابتك رجاء اكتب'نعم' وان لم تكن اجابتك رجاء اكتب اجابتك هنا : \n")
    if ans =="نعم":
        answer=text
        text_length=len(text.split())
        if text_length < (question_time_limit/5):
            ev_score=0.01
        elif text_length < (question_time_limit/4):
            ev_score=0.02
        elif text_length < (question_time_limit/3):
            ev_score=0.03
        elif text_length < (question_time_limit/2):
            ev_score=0.04
        else:
            ev_score=0.05
    else:
        answer=ans
        time_y=time.time()-time_x
        if(time_y < 5):
            ev_score=0
        elif(time_y > 2*question_time_limit):
            ev_score=0.025
        else:
            ev_score=0.05
    
    return answer,ev_score


def grammer_check_english(texts):
    # return 3 parameters 
    # first is the comment depends on the number of errors in the text
    #second is the grammatical and spelling errors in the text with thier replacement
    #third is the number of errors which will be evaluated in the final score 
    matches = tool_en.check(texts)
    number_of_errors=0 
    missing_corr=[]
    my_mistakes=[]
    my_corrections=[]
    for rules in matches:
        if len(rules.replacements)>0:
            my_mistakes.append(texts[rules.offset:rules.errorLength+rules.offset])
            my_corrections.append(rules.replacements[0])
            missing_corr=list(zip(my_mistakes,my_corrections))
            number_of_errors+=1
    score=max(0.2-(number_of_errors-5)/100,0)
    score=min(0.2,score)
    #if score > 0.15:
    #    comment=""
    #elif  score > 0.1 :
    #    comment="Try to avoid grammar and spelling mistakes"
    #elif score >0.5:
    #    comment="You must improve your English"
    #else:
    #    comment="your English is very bad"
    return score,missing_corr



def grammer_check_arabic(texts):
    # return 3 parameters 
    # first is the comment depends on the number of errors in the text
    #second is the grammatical and spelling errors in the text with thier replacement
    #third is the number of errors which will be evaluated in the final score 
    matches = tool_ar.check(texts)
    number_of_errors=0 
    my_mistakes=[]
    my_corrections=[]
    for rules in matches:
        if len(rules.replacements)>0:
            my_mistakes.append(texts[rules.offset:rules.errorLength+rules.offset])
            my_corrections.append(rules.replacements[0])
            mis_corr=list(zip(my_mistakes,my_corrections))
            number_of_errors+=1
    
    score=max(0.2-(number_of_errors-1)/100,0)
    score=min(score,0.2)
    #if score > 0.15:
        #comment=""
    #elif  score > 0.1 :
        #comment="حاول ان تتجنب الاخطاء الاملائيه والنحويه"
    #elif score >0.5:
        #comment="يجب ان تحسن لغتك العربيه"
    #else:
        #comment="لغتك العربيه سيئه للغايه"
    return score,mis_corr



def get_first_name(texts):
     #return the first name mentioned in a text or "" which indicates that no name is mentioned 
    x=pos_tag(texts.split())
    name=""
    for z in x:
        if z[1] == 'NNP':
            name=z[0]
            break
        if z[1] == 'JJ':
            name=z[0]
            break
    return name


# In[5]:


# the types of evaluations 
# make the number of words into account and the time for writing in case of writing into account 
# type 1 : rouge for the technical parts ,sequence matcher for plagiarism check ch
#plagiarism check
#if ratio>0.6 then there will be big plagiarism ratio and it's not acceptable
def plagiarism_checker(interviewer_text,sample_answer_text):
    return SequenceMatcher(None,sample_answer_text,interviewer_text).ratio()

#for precision score in bad answer if it's > 0.8 then the answer is bad = 75% of the function weight 
#meaning that it will be 2.5% out of 10 % of the total score of the question otherwise it has no effect
#as the precision score here represents how much of the bad answer in the expected answer 
#for the normal cases if the the answer is between 15% to 25% f score then it will be 2.5% out of 10%
#if between 25% and 35% f score will be 0% if it's 35%:40% the f score will be 7.5% out of 10% and if the score >40% 
#the final score will be 10% out of 10%

def rouge_scores_ev (expected_ans,reference_ans,why="normal"):
    scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)
    scores = scorer.score(expected_ans,reference_ans)
    precision_score=scores['rouge1'][0]#precision
    recall_score=scores['rouge1'][1]#recall
    f_score=scores['rouge1'][2]#f_score
    if why=="bad answer":
        return precision_score
    elif why == "recall":
        return recall_score
    else:
        return f_score


def rouge_scores_evaluation(sample_answer_score,bad_answer_score): 
    
    if sample_answer_score < 0.05:
        total_score=0.1
    elif sample_answer_score < 0.10:
        total_score=0.2
    elif sample_answer_score < 0.15:
        total_score=0.3
    elif sample_answer_score < 0.20:
        total_score=0.4
    elif sample_answer_score < 0.25:
        total_score=0.5
    elif sample_answer_score < 0.30:
        total_score=0.6
    elif sample_answer_score < 0.35:
        total_score=0.7
    elif sample_answer_score < 0.4:
        total_score=0.8
    elif sample_answer_score < 0.45:
        total_score=0.9
    elif sample_answer_score < 0.50:
        total_score=0.95
    else:
        total_score=1.0
    if bad_answer_score >=0.8:
        total_score=min(0.25,total_score)
    return total_score


#inside the for loop
#sample_answer_score=[]
#bad_answer_score=[]
#interviewer_ans="i'm the best in the world and i want to be the best fighter too as i'm ambitious "
#ref_sample=question_and_sample_answers[questions_expected_g[0]]
#bad_answers=question_and_bad_answers[questions_expected_b[0]]
#for reference_ans in ref_sample[0]:
#    sample_answer_score.append(rouge_scores_ev(interviewer_ans,reference_ans))
#    pla_ch=plagiarism_checker(interviewer_ans,reference_ans)
#    if pla_ch > 0.6:
#        print("don't just copy and past the answer from the internet")
#    for reference_ans in bad_answers[0]:
#        bad_answer_score.append(rouge_scores_ev(interviewer_ans,reference_ans,"bad answer"))
#sample_answer_scores=max(sample_answer_score)
#bad_answer_scores=max(bad_answer_score)
#rouge_evaluation=rouge_scores_evaluation(sample_answer_scores,bad_answer_scores)


# In[6]:


# classification evaluation %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# classification evaluation %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def worry_classification(text=""):
    #we will use recall from rouge score
    feel_list=[]
    ro_sc_list=[]
    with open ("worring.txt","r",encoding='utf8') as f:
        text_lines=f.readlines()
        for line in text_lines:
            feel_list.append(line)
    f.close()
    for feel in feel_list:
        ro_sc_list.append(rouge_scores_ev(text,feel,why="recall"))
    return 1-max(ro_sc_list)
        
    

def ambitious_classification(text=""):
    feel_list=[]
    ro_sc_list=[]
    with open ("ambitious.txt","r",encoding='utf8') as f:
        text_lines=f.readlines()
        for line in text_lines:
            feel_list.append(line)
    f.close()
    for feel in feel_list:
        ro_sc_list.append(rouge_scores_ev(text,feel,why="recall"))
    return max(ro_sc_list)


def vanity_classification(text=""):
    feel_list=[]
    ro_sc_list=[]
    with open ("vanity.txt","r",encoding='utf8') as f:
        text_lines=f.readlines()
        for line in text_lines:
            feel_list.append(line)
    f.close()
    for feel in feel_list:
        ro_sc_list.append(rouge_scores_ev(text,feel,why="recall"))
    return 1-max(ro_sc_list)


def greedy_classification(text=""):
    feel_list=[]
    ro_sc_list=[]
    with open ("greedy.txt","r",encoding='utf8') as f:
        text_lines=f.readlines()
        for line in text_lines:
            feel_list.append(line)
    f.close()
    for feel in feel_list:
        ro_sc_list.append(rouge_scores_ev(text,feel,why="recall"))
    return 1-max(ro_sc_list)


def loyalty_classification(text=""):
    feel_list=[]
    ro_sc_list=[]
    with open ("loyalty.txt","r",encoding='utf8') as f:
        text_lines=f.readlines()
        for line in text_lines:
            feel_list.append(line)
    f.close()
    for feel in feel_list:
        ro_sc_list.append(rouge_scores_ev(text,feel,why="recall"))
    return max(ro_sc_list)


# In[7]:


#English
#the input to this function which calculate the score of each question individualy 
# high score from 80% to 100% , low score frome 0% to 40 % average score from 40% to 80%
# input is like that:
# 1- the interviewee answer
# 2- good samples answers from the internet
# 3- bad samples answers from the internet
# 4- the score of the time which is an output of get_the_answer_from_the_user_english function
# 5- rouge weight for this question
# 6- worry weight for this question
# 7- ambitious weight for this question 
# 8- gready weights for this question
# 9- loyalty weight for this question 
# 10- vanity weight for this question
# and returns the following
# 1- the final score of the question
# 2- grammar_score
# 3- grammar mistakes and corrections
# 4- time score
# 5- rouge score
# 6- worry_score
# 7- ambitious score
# 8- gready score
# 9- loyalty score
# 10- vanity_score

def evaluation_of_single_answer_english(answer,good_samples,bad_samples,time_score,rouge_weight,worry_weight,ambitious_weight,greedy_weight,loyalty_weight,vanity_weight):
    plagiarism_list=[]
    good_rouge_score_list=[]
    bad_rouge_score_list=[]
    grammar_score,mistake_correction = grammer_check_english(answer)
    for sample in good_samples:
        plagiarism_list.append(plagiarism_checker(answer,sample))
        good_rouge_score_list.append(rouge_scores_ev(answer,sample,"normal"))
    for sample in bad_samples:
        bad_rouge_score_list.append (rouge_scores_ev(answer,sample,"bad answer"))
    if (max(plagiarism_list)>0.6) or (time_score==0):
        question_score=0
        return question_score,0,[0],0,0,0,0,0,0,0
    
    try:
        rouge_score=rouge_weight * rouge_scores_evaluation(max(good_rouge_score_list),max(bad_rouge_score_list))
    except:
        print("unexpected error in rouge score")
    time_score=time_score
    question_score=grammar_score+time_score+rouge_score
    worry_score=worry_weight * worry_classification(answer)
    ambitious_score=ambitious_weight * ambitious_classification(answer)
    greedy_score=greedy_weight * greedy_classification(answer)
    loyalty_score=loyalty_weight * loyalty_classification(answer)
    vanity_score=vanity_weight * vanity_classification(answer)
    question_score=grammar_score+time_score+rouge_score+worry_score+ambitious_score+greedy_score+loyalty_score+vanity_score
    return question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score
    
        
    
    
        
def feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score):
    flage=0
    flage2=0
    mistake_correction_comment=""
    if question_score > 0.50:
        question_comment="you are doing well"
        flage2=1
    elif question_score==0:
        question_comment="we think you have cheated in this question that's why your score = 0%"
        flage=1
    else:
        question_comment="you need to work on yourself more than that"
    if grammar_score > 0.10:
        grammar_comment=""
    else:
        grammar_comment=". Howerver, you need to improve your English"
    if time_score <= 0.01:
        time_score_comment=", you spent too much time answering"
    else:
        time_score_comment=""
    if rouge_score > 0.10 or flage2==1:
        rouge_comment=""
    else:
        rouge_comment=", consider that your answer is far away from being good answer"
    if worry_score < 0.02:
        worry_comment=", You don't have to be nervous, calm down"
    else:
        worry_comment=""
    if vanity_score <0.02:
        vanity_comment=".Moreover, you need to think about the company more than thinking about yourself"
    else:
        vanity_comment=""
    if greedy_score<0.02:
        greedy_comment=", you do not need to show the interviewer that you are eager for money"
    else:
        greedy_comment=""
    if ambitious_score>0.1:
        ambitious_comment=", and it is great to show the interviewer that you have a future vision and ambition"
    else:
        ambitious_comment=""
    if loyalty_score>0.1:
        loyalty_comment=", and it is great to show the interviewer that you are loyal to the company"
    else:
        loyalty_comment=""
    for i in range(0,len(mistake_correction)):
        mistake_correction_comment=mistake_correction_comment+"("+ mistake_correction[i][0]+","+mistake_correction[i][1] + "),"
    if flage==1:
        return question_comment,mistake_correction_comment
    else:
        return question_comment+loyalty_comment+time_score_comment+ambitious_comment+grammar_comment+rouge_comment+greedy_comment+vanity_comment,mistake_correction_comment
    


# In[8]:


#the bage after answering all the questions consists of main feed back shown at the beginning 
#the buttons at the evaluation 
#1- button for how to answer the question
#2- button for the feedback
#3- button for the next question move to the next page
#4- button for the grammatical and spelling mistakes 
#5- button for good sample answer
#6- button for question score 
#7- button for bad answer


# In[9]:


global normal 
normal = interview("normal")
global demo 
demo = interview("demo")


# In[10]:


def english_demo_interview(number_of_questions=5):
    number_of_wrong_recognition=0
    total_score_weighted=0
    total_score=0
    questions_expected,question_and_sample_answer,question_and_how_to_answer,question_and_question_weight,question_and_worry_mental_state_weight,question_and_ambitious_mental_state_weight,question_and_greedy_mental_state_weight,question_and_loyalty_mental_state_weight,question_and_vanity_mental_state_weight,question_and_rouge_score_weight,question_and_good_sample_answers,question_and_bad_answers,question_and_time_limit=load_question_dataset()
    list_of_w=[0.05,0.1,0.15,0.2,0.25,0.30,0.35]
    list_of_q=[]
    for i in range(0,len(questions_expected)):
        demo.add_question_and_model_answer(questions_expected[i],question_and_sample_answer[questions_expected[i]],question_and_bad_answers[questions_expected[i]],question_and_how_to_answer[questions_expected[i]],question_and_time_limit[questions_expected[i]],question_and_question_weight[questions_expected[i]])
    #############################################
    question1=questions_expected[0]
    question=question1
    speak_the_questionss=speak_text_english(question,question)
    interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=total_score+question_score 
    print("Score results as following")
    print("Question score  ",demo.rouge_score_ev[question])
    print("Grammar score ",demo.grammar_score_ev[question])
    print("time score ",demo.time_score_ev[question])
    print("worry score ",demo.worry_score_ev[question])
    print("greedy score ",demo.greedy_score_ev[question])
    print("ambitious score ",demo.ambitious_score_ev[question])
    print("vanity score ",demo.vanity_score_ev[question])
    print("loyalty score ",demo.loyalty_score_ev[question])
    ############################################    
    question2=questions_expected[1]
    question=question2
    speak_the_questionss=speak_text_english(question,question)
    interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=(total_score+question_score)/2
    print("Score results as following")
    print("Question score  ",demo.normal.rouge_score_ev[question])
    print("Grammar score ",demo.grammar_score_ev[question])
    print("time score ",demo.time_score_ev[question])
    print("worry score ",demo.worry_score_ev[question])
    print("greedy score ",demo.greedy_score_ev[question])
    print("ambitious score ",demo.ambitious_score_ev[question])
    print("vanity score ",demo.vanity_score_ev[question])
    print("loyalty score ",demo.loyalty_score_ev[question])
    #################################################
    if total_score < 0.4:#weak state
        question3=questions_expected[2]
        question=question3
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score 
        print("Score results as following")
        print("Question score  ",demo.normal.rouge_score_ev[question])
        print("Grammar score ",demo.grammar_score_ev[question])
        print("time score ",demo.time_score_ev[question])
        print("worry score ",demo.worry_score_ev[question])
        print("greedy score ",demo.greedy_score_ev[question])
        print("ambitious score ",demo.ambitious_score_ev[question])
        print("vanity score ",demo.vanity_score_ev[question])
        print("loyalty score ",demo.loyalty_score_ev[question])
        ###########################################
        question4=questions_expected[3]
        question=question4
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score 
        print("Score results as following")
        print("Question score  ",demo.normal.rouge_score_ev[question])
        print("Grammar score ",demo.grammar_score_ev[question])
        print("time score ",demo.time_score_ev[question])
        print("worry score ",demo.worry_score_ev[question])
        print("greedy score ",demo.greedy_score_ev[question])
        print("ambitious score ",demo.ambitious_score_ev[question])
        print("vanity score ",demo.vanity_score_ev[question])
        print("loyalty score ",demo.loyalty_score_ev[question])
        ###########################################
    elif total_score < 0.7: #average_state
        question3==questions_expected[4]
        question=question3
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score
        print("Score results as following")
        print("Question score  ",demo.normal.rouge_score_ev[question])
        print("Grammar score ",demo.grammar_score_ev[question])
        print("time score ",demo.time_score_ev[question])
        print("worry score ",demo.worry_score_ev[question])
        print("greedy score ",demo.greedy_score_ev[question])
        print("ambitious score ",demo.ambitious_score_ev[question])
        print("vanity score ",demo.vanity_score_ev[question])
        print("loyalty score ",demo.loyalty_score_ev[question])
        ##########################################
        question4=questions_expected[5]
        question=question4
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score
        print("Score results as following")
        print("Question score  ",demo.normal.rouge_score_ev[question])
        print("Grammar score ",demo.grammar_score_ev[question])
        print("time score ",demo.time_score_ev[question])
        print("worry score ",demo.worry_score_ev[question])
        print("greedy score ",demo.greedy_score_ev[question])
        print("ambitious score ",demo.ambitious_score_ev[question])
        print("vanity score ",demo.vanity_score_ev[question])
        print("loyalty score ",demo.loyalty_score_ev[question])
        ############################################
    else:#strong state
        question3=questions_expected[6]
        question=question3
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition = get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score
        print("Score results as following")
        print("Question score  ",demo.normal.rouge_score_ev[question])
        print("Grammar score ",demo.grammar_score_ev[question])
        print("time score ",demo.time_score_ev[question])
        print("worry score ",demo.worry_score_ev[question])
        print("greedy score ",demo.greedy_score_ev[question])
        print("ambitious score ",demo.ambitious_score_ev[question])
        print("vanity score ",demo.vanity_score_ev[question])
        print("loyalty score ",demo.loyalty_score_ev[question])
        ################################################
        question4=questions_expected[7]
        question=question4
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score
        print("Score results as following")
        print("Question score  ",demo.normal.rouge_score_ev[question])
        print("Grammar score ",demo.grammar_score_ev[question])
        print("time score ",demo.time_score_ev[question])
        print("worry score ",demo.worry_score_ev[question])
        print("greedy score ",demo.greedy_score_ev[question])
        print("ambitious score ",demo.ambitious_score_ev[question])
        print("vanity score ",demo.vanity_score_ev[question])
        print("loyalty score ",demo.loyalty_score_ev[question])
        ###############################################
    question5=questions_expected[11]
    question=question5
    speak_the_questionss=speak_text_english(question,question)
    interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=total_score+question_score
    print("Score results as following")
    print("Question score  ",demo.normal.rouge_score_ev[question])
    print("Grammar score ",demo.grammar_score_ev[question])
    print("time score ",demo.time_score_ev[question])
    print("worry score ",demo.worry_score_ev[question])
    print("greedy score ",demo.greedy_score_ev[question])
    print("ambitious score ",demo.ambitious_score_ev[question])
    print("vanity score ",demo.vanity_score_ev[question])
    print("loyalty score ",demo.loyalty_score_ev[question])
    ###############################################
    question6=questions_expected[10]
    question=question6
    speak_the_questionss=speak_text_english(question,question)
    interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(demo.time_limit[question],number_of_wrong_recognition)
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    demo.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=total_score+question_score
    avg_total_score= (total_score/6)*100
    print("Score results as following")
    print("Question score  ",demo.normal.rouge_score_ev[question])
    print("Grammar score ",demo.grammar_score_ev[question])
    print("time score ",demo.time_score_ev[question])
    print("worry score ",demo.worry_score_ev[question])
    print("greedy score ",demo.greedy_score_ev[question])
    print("ambitious score ",demo.ambitious_score_ev[question])
    print("vanity score ",demo.vanity_score_ev[question])
    print("loyalty score ",demo.loyalty_score_ev[question])
    print("Total score ",avg_total_score)
    number_of_wrong_recognition=0


# In[11]:


def english_normal_interview(number_of_questions=5):
    total_score_weighted=0
    total_score=0
    number_of_wrong_recognition=0
    questions_expected,question_and_sample_answer,question_and_how_to_answer,question_and_question_weight,question_and_worry_mental_state_weight,question_and_ambitious_mental_state_weight,question_and_greedy_mental_state_weight,question_and_loyalty_mental_state_weight,question_and_vanity_mental_state_weight,question_and_rouge_score_weight,question_and_good_sample_answers,question_and_bad_answers,question_and_time_limit=load_question_dataset()
    list_of_w=[0.05,0.1,0.15,0.2,0.25,0.30,0.35]
    list_of_q=[]
    for i in range(0,len(questions_expected)):
        normal.add_question_and_model_answer(questions_expected[i],question_and_sample_answer[questions_expected[i]],question_and_bad_answers[questions_expected[i]],question_and_how_to_answer[questions_expected[i]],question_and_time_limit[questions_expected[i]],question_and_question_weight[questions_expected[i]])
    #############################################
    question1=questions_expected[0]
    question=question1
    speak_the_questionss=speak_text_english(question,question)
    interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=total_score+question_score 
    ############################################    
    question2=normal.get_question(0.20)
    if question2 == questions_expected[0]:
        question2=normal.get_question(0.20)
    question=question2
    speak_the_questionss=speak_text_english(question,question)
    interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=(total_score+question_score)/2
    #################################################
    if total_score < 0.4:#weak state
        question3=normal.get_question(0.15)
        question=question3
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score 
        ###########################################
        question4=normal.get_question(0.10)
        if question4 == questions_expected[10]:
            question4=normal.get_question(0.10)
        question=question4
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score 
        ###########################################
    elif total_score < 0.7: #average_state
        question3==normal.get_question(0.10)
        if question3==questions_expected[10]:
            question3=normal.get_question(0.10)
        question=question3
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score
        ##########################################
        question4=normal.get_question(0.20)
        if question4 == questions_expected[0]:
            question4=normal.get_question(0.20)
        question=question4
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score 
        ############################################
    else:#strong state
        question3=normal.get_question(0.25)
        question=question3
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score 
        ################################################
        question4=normal.get_question(0.10)
        if question4 == questions_expected[10]:
            question4=normal.get_question(0.10)  
        question=question4
        speak_the_questionss=speak_text_english(question,question)
        interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
        question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
        feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
        #the following line will be shown for each quesion at the final after ending the interview
        normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
        total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
        total_score=total_score+question_score
        ###############################################
    question5=normal.get_question(0.20)
    if question5 == questions_expected[0]:
        question5=normal.get_question(0.20)
    question=question5
    speak_the_questionss=speak_text_english(question,question)
    interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=total_score+question_score 
    ###############################################
    question6=questions_expected[10]
    question=question6
    speak_the_questionss=speak_text_english(question,question)
    interviewee_answer,Time_score,number_of_wrong_recognition=get_the_answer_from_the_user_english(normal.time_limit[question],number_of_wrong_recognition)
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    normal.evaluation_add(question,question_score,mistake_correction,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=total_score+question_score
    
    
    


# In[12]:


english_demo_interview()


# In[ ]:




