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
#from nltk import pos_tag
#import nltk
#nltk.download('averaged_perceptron_tagger')
import language_tool_python
tool_en = language_tool_python.LanguageTool('en-US')
tool_ar = language_tool_python.LanguageTool('ar-EG')
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
#from keras.models import load_model
#from keras.preprocessing.text import Tokenizer
#from keras.preprocessing.sequence import pad_sequences
#import numpy as np


# In[2]:


root= Tk()


# In[3]:


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
        self.que_weightss={} # save the weights of the question on it 
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
        self.que_weightss[question]=qe_weight
        
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
    def evaluation_add(self,question,ansxyz,question_score,mistake_correction,feedback_to_answer,wor_score,amb_score,greed_score,loy_score,van_score,rog_score,gr_score,ti_score):
        self.interview_interviewer_answer[question]=ansxyz
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
        


# In[4]:


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


# In[5]:


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
            said="your answer hasn't been recorded please remove this text and write your answer"
        try:
            said=r.recognize_google(audio)
        except Exception as e:
            said="your answer hasn't been recorded please remove this text and write your answer"
    
    
    return said




#input is the text and output is the list of sentences
def split_sentence_for_classification(text):    
    words=text.split()
    sent_class_gui=[]
    for i in range(0,len(words),3):
        sent_count_gui=min(5,len(words)-i)
        sent_class_gui.append(" ".join(words[i:i+sent_count_gui]))
    return sent_class_gui


# In[6]:


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


def plagiarism_checker(interviewer_text,sample_answer_text):
    return SequenceMatcher(None,sample_answer_text,interviewer_text).ratio()



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

#return the final score for rouge valuation after both good and bad sample answers 
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
    score=max(0.2-(number_of_errors)/100,0)
    score=min(0.2,score)
    return score,missing_corr



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
    


# In[7]:


# create second window for evaluation 
def Evaluation():
    global Eval
    global qeval
    global Question_eval
    global toppart
    global bottompart
    global next_button
    global prev_button
    global question_gui
    global demo
    global question_gui_list
    global total_score_weighted
    for widget in root.winfo_children():
        widget.destroy()
    q_c=0
    for question_gui_dis in question_gui_list:
        ans_apk=demo.interview_interviewer_answer[question_gui_dis]
        Label(root,text="Question: "+question_gui_dis,font = ("Comic Sans MS", 12)).grid()
        q_c+=1
        #time.sleep(1)
        Label(root,text="Your Answer: "+ans_apk ,font = ("Comic Sans MS", 12)).grid()
        #time.sleep(1)
        q_c+=1
    q_c=0
    Label(root,text="Total score = "+str(total_score_weighted*100),font = ("Comic Sans MS", 20)).grid()
    Eval = Toplevel()
    Eval.geometry("1028x1100")
    Eval.resizable(height =0,width =0)
    Eval.grab_set()
    
    s = ttk.Style()
    s.configure('TNotebook.Tab', font=('URW Gothic L','12') )
    
    toppart = LabelFrame(Eval)
    toppart.grid(row = 2, column= 0, columnspan=5,padx=20,pady =20, sticky = W, ipady = 10, ipadx = 5)
    
    text_out = question_gui_list[qeval]
    Question_eval = Label(toppart, text= text_out,  font = ('URW Gothic L', 12))
    Question_eval.grid(row=0,column=0, rowspan = 3,padx=10, pady = 5, sticky = W)
    
    next_button= Button(toppart, text="Next Question",padx = 10,pady = 5,font=('URW Gothic L', 11) ,command = next_qeval)
    next_button.grid(row=4,column=0)
    prev_button= Button(toppart, text="Previous Question",padx = 10,pady = 5,font=('URW Gothic L', 11) ,command = past_qeval)
    prev_button.grid(row=5,column=0)
    prev_button["state"] = "disabled"
    
    bottompart= LabelFrame(Eval)
    bottompart.grid(row = 5, column=0, sticky = W,padx=10, pady = 10)
    question_gui=question_gui_list[qeval]
    global tabControl
    tabControl = ttk.Notebook(bottompart)
    
    global tab1
    global tab2
    global tab3
    global tab4
    global tab5
    
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tab4 = ttk.Frame(tabControl)
    tab5 = ttk.Frame(tabControl)
    
    tabControl.add(tab1, text ='FeedBack' )
    tabControl.add(tab2, text ='Tips to answer')
    tabControl.add(tab3, text ='Best answer')
    tabControl.add(tab4, text ='Gramatical errors with corrections')
    tabControl.add(tab5, text ='Question Score')
    tabControl.pack(expand = 1, fill ="both")

    fb_gui=tkinter.Text(tab1, 
            font = ("Comic Sans MS", 12))
    fb_gui.grid(column = 0,  
                                   row = 0,
                                   padx = 50,
                                   pady = 50)
    fb_gui.config(state="normal")
    fb_gui.insert(tkinter.INSERT,demo.feedback_ev[question_gui_list[qeval]])
    fb_gui.config(state="disabled")
    gl_gui=tkinter.Text(tab2,
              font = ("Comic Sans MS", 12))
    gl_gui.grid(column = 0,
                                        row = 0, 
                                        padx = 50,
                                        pady = 50)
    gl_gui.config(state="normal")
    gl_gui.insert(tkinter.INSERT,question_and_how_to_answer[question_gui_list[qeval]])
    gl_gui.config(state="disabled")
    ga_gui=tkinter.Text(tab3,
              font = ("Comic Sans MS", 12))
    ga_gui.grid(column = 0,
                                        row = 0, 
                                        padx = 50,
                                        pady = 50)
    ga_gui.config(state="normal")
    ga_gui.insert(tkinter.INSERT,demo.interview_model_question_answers[question_gui_list[qeval]])
    ga_gui.config(state="disabled")
    grsp_gui=tkinter.Text(tab4,
              font = ("Comic Sans MS", 12))
    grsp_gui.grid(column = 0,
                                        row = 0, 
                                        padx = 50,
                                        pady = 50)
    grsp_gui.config(state="normal")
    grsp_gui.insert(tkinter.INSERT,demo.grammar_miss_corr_ev[question_gui_list[qeval]])
    grsp_gui.config(state="disabled")
    sc_ev_gui=tkinter.Text(tab5,
              font = ("Comic Sans MS", 12) )
    sc_ev_gui.grid(column = 0,
                                        row = 0, 
                                        padx = 50,
                                        pady = 50)
    sc_ev_gui.config(state="normal")
    sc_ev_gui.insert(tkinter.INSERT,str(demo.question_Score_ev[question_gui_list[qeval]]*100 ) + " %")
    sc_ev_gui.config(state="disabled")
    # we will add the feeling weights in the future to get the final score in percentages 100%
    a=Label(root,text="Question: "+question_gui_list[qeval]+" rouge score= "+str(demo.rouge_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    b=Label(root,text="Question: "+question_gui_list[qeval]+" worry score= "+str(demo.worry_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    c=Label(root,text="Question: "+question_gui_list[qeval]+" ambitious score= "+str(demo.ambitious_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    d=Label(root,text="Question: "+question_gui_list[qeval]+" vanity score = "+str(demo.vanity_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    aa=Label(root,text="Question: "+question_gui_list[qeval]+" greedy score= "+str(demo.greedy_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    bb=Label(root,text="Question: "+question_gui_list[qeval]+" loyal score= "+str(demo.loyalty_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    a.grid()
    b.grid()
    c.grid()
    d.grid()
    aa.grid()
    bb.grid()
def show_label():
    global tabControl
    global tab1
    global tab2
    global tab3
    global tab4
    global tab5
    global Eval
    global qeval
    global Question_eval
    global toppart
    global bottompart
    global next_button
    global prev_button
    global feedback
    global question_gui
    tabControl.pack_forget()
    tabControl = ttk.Notebook(bottompart)
    
    tab1.grid_forget()
    
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tab4 = ttk.Frame(tabControl)
    tab5 = ttk.Frame(tabControl)
    
    tabControl.add(tab1, text ='FeedBack' )
    tabControl.add(tab2, text ='Tips to answer')
    tabControl.add(tab3, text ='Best answer')
    tabControl.add(tab4, text ='Gramatical errors with correction')
    tabControl.add(tab5, text ='Question Score')
    tabControl.pack(expand = 1, fill ="both")

    fb_gui=tkinter.Text(tab1, 
            font = ("Comic Sans MS", 12))
    fb_gui.grid(column = 0,  
                                   row = 0,
                                   padx = 50,
                                   pady = 50)
    fb_gui.config(state="normal")
    fb_gui.insert(tkinter.INSERT,demo.feedback_ev[question_gui_list[qeval]])
    fb_gui.config(state="disabled")
    gl_gui=tkinter.Text(tab2,
              font = ("Comic Sans MS", 12))
    gl_gui.grid(column = 0,
                                        row = 0, 
                                        padx = 50,
                                        pady = 50)
    gl_gui.config(state="normal")
    gl_gui.insert(tkinter.INSERT,question_and_how_to_answer[question_gui_list[qeval]])
    gl_gui.config(state="disabled")
    ga_gui=tkinter.Text(tab3,
              font = ("Comic Sans MS", 12))
    ga_gui.grid(column = 0,
                                        row = 0, 
                                        padx = 50,
                                        pady = 50)
    ga_gui.config(state="normal")
    ga_gui.insert(tkinter.INSERT,demo.interview_model_question_answers[question_gui_list[qeval]])
    ga_gui.config(state="disabled")
    grsp_gui=tkinter.Text(tab4,
              font = ("Comic Sans MS", 12))
    grsp_gui.grid(column = 0,
                                        row = 0, 
                                        padx = 50,
                                        pady = 50)
    grsp_gui.config(state="normal")
    grsp_gui.insert(tkinter.INSERT,demo.grammar_miss_corr_ev[question_gui_list[qeval]])
    grsp_gui.config(state="disabled")
    sc_ev_gui=tkinter.Text(tab5,
              font = ("Comic Sans MS", 12) )
    sc_ev_gui.grid(column = 0,
                                        row = 0, 
                                        padx = 50,
                                        pady = 50)
    sc_ev_gui.config(state="normal")
    sc_ev_gui.insert(tkinter.INSERT,str(demo.question_Score_ev[question_gui_list[qeval]]*100 ) + " %")
    sc_ev_gui.config(state="disabled")
    a=Label(root,text="Question: "+question_gui_list[qeval]+" rouge score= "+str(demo.rouge_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    b=Label(root,text="Question: "+question_gui_list[qeval]+" worry score= "+str(demo.worry_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    c=Label(root,text="Question: "+question_gui_list[qeval]+" ambitious score= "+str(demo.ambitious_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    d=Label(root,text="Question: "+question_gui_list[qeval]+" vanity score = "+str(demo.vanity_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    aa=Label(root,text="Question: "+question_gui_list[qeval]+" greedy score= "+str(demo.greedy_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    bb=Label(root,text="Question: "+question_gui_list[qeval]+" loyal score= "+str(demo.loyalty_score_ev[question_gui_list[qeval]]*100)+"%",font = ("Comic Sans MS", 12))
    a.grid()
    b.grid()
    c.grid()
    d.grid()
    aa.grid()
    bb.grid()
    

def past_qeval():
    
    global qeval
    global Question_eval
    global toppart
    global prev_button
    global next_button
    qeval = qeval - 1
    Question_eval.grid_forget()
    text_out = question_gui_list[qeval]
    Question_eval = Label(toppart, text= text_out,  font = ('URW Gothic L', 12))
    Question_eval.grid(row=0,column=0, rowspan = 3,padx=10,sticky = W)
    next_button["state"] = "normal"        
    if qeval == 0 :
        prev_button["state"] = "disabled"
    show_label()
    
    
def next_qeval():
    
    global qeval
    global Question_eval
    global toppart
    global next_button
    global prev_button
    qeval = qeval + 1
    Question_eval.grid_forget()
    text_out = question_gui_list[qeval]
    Question_eval = Label(toppart, text= text_out,  font = ('URW Gothic L', 12))
    Question_eval.grid(row=0,column=0, rowspan = 3,padx=10,sticky = W)
    prev_button["state"] = "normal"
    if qeval >= len(question_gui_list)-1 :
        #end the program with THANK you 
        next_button["state"] = "disabled"
    show_label()
    


# In[8]:


#global variables
global demo
global question_gui
global total_score_weighted
global question_gui_list
global e
global start_pb   
global question_desplayed_number_gui
global number_of_questions_gui
global start_frame 
global start_pb 
global demo_frame 
global question_desplayed_number_gui
global total_score_weighted
global total_score
global time_x
global questions_expected
global question_and_sample_answer
global question_and_how_to_answer
global question_and_question_weight
global question_and_worry_mental_state_weight
global question_and_ambitious_mental_state_weight
global question_and_greedy_mental_state_weight 
global question_and_loyalty_mental_state_weight
global question_and_vanity_mental_state_weight 
global question_and_rouge_score_weight 
global question_and_good_sample_answers
global question_and_bad_answers
global question_and_time_limit
global Eval
global qeval
global Question_eval
global toppart
global bottompart
global next_button
global prev_button
global question_gui
qeval=0
total_score_weighted=0
total_score=0
number_of_questions_gui=2
question_desplayed_number_gui=0
question_gui_list=[]
questions_expected,question_and_sample_answer,question_and_how_to_answer,question_and_question_weight,question_and_worry_mental_state_weight,question_and_ambitious_mental_state_weight,question_and_greedy_mental_state_weight,question_and_loyalty_mental_state_weight,question_and_vanity_mental_state_weight,question_and_rouge_score_weight,question_and_good_sample_answers,question_and_bad_answers,question_and_time_limit=load_question_dataset()
demo=interview("demo")
for i in range(0,len(questions_expected)):
    demo.add_question_and_model_answer(questions_expected[i],question_and_sample_answer[questions_expected[i]],question_and_bad_answers[questions_expected[i]],question_and_how_to_answer[questions_expected[i]],question_and_time_limit[questions_expected[i]],question_and_question_weight[questions_expected[i]])
    #############################################
#question_gui_list.append(demo.interview_questions[0])
#question_gui_list.append(demo.interview_questions[4])
question_gui_list.append(demo.interview_questions[11])
question_gui_list.append(demo.interview_questions[9])
#question_gui_list.append(demo.interview_questions[10])


# In[9]:


def enter_text_gui():
    global demo
    global question_gui
    global total_score_weighted
    global question_gui_list
    global e
    global start_pb   
    global question_desplayed_number_gui
    global number_of_questions_gui
    global start_frame 
    global start_pb 
    global demo_frame 
    global question_desplayed_number_gui
    global total_score_weighted
    global total_score
    global time_x
    global questions_expected
    global question_and_sample_answer
    global question_and_how_to_answer
    global question_and_question_weight
    global question_and_worry_mental_state_weight
    global question_and_ambitious_mental_state_weight
    global question_and_greedy_mental_state_weight 
    global question_and_loyalty_mental_state_weight
    global question_and_vanity_mental_state_weight 
    global question_and_rouge_score_weight 
    global question_and_good_sample_answers
    global question_and_bad_answers
    global question_and_time_limit
    global Eval
    global qeval
    global Question_eval
    global toppart
    global bottompart
    global next_button
    global prev_button
    global question_gui
    global question_desplayed_number_gui
    global number_of_questions_gui
    #start_pb['state']='disable'
    global time_x
    global question_gu
    root.geometry("1920x1080")
    for widget in root.winfo_children():
        widget.destroy()
    time_x=time.time()
    question_gu=question_gui_list[question_desplayed_number_gui]
    speak=speak_text_english(question_gu,question_gu)
    question_desplayed_number_gui=question_desplayed_number_gui+1
    question_label=Label(root, text="Question "+str(6-number_of_questions_gui)+": "+question_gu,font=("Comic Sans MS", 12)).grid(row=0,column=0,sticky=W, rowspan=5)
    answer_label=Label(root, text="Find your answer attached below ,feel free to edit it as much as you want but consider that the time of editing is included in the evaluation ",font=("Comic Sans MS", 12)).grid(row=10,column=0,sticky=W, rowspan=5)
    
    interveiwee_answer_gui=get_audio_english(demo.time_limit[question_gu])
    e=Entry(root,width=200)
    e.grid(row=20,column=0)
    e.insert(0,interveiwee_answer_gui)
    interviewee_answers_expected=e.get()
    time.sleep(1)
    enter_text=Button(root,text="Submit",padx=10,pady=10,command=lambda :record_interviewee_answer(question_gu,interviewee_answers_expected)).grid(row=35,column=0)
    

def record_interviewee_answer(qustion,anser):
    global number_of_questions_gui
    global question_desplayed_number_gui
    global time_x
    global question_gu
    global demo
    global question_gui
    global total_score_weighted
    global question_gui_list
    global e
    global start_pb   
    global question_desplayed_number_gui
    global number_of_questions_gui
    global start_frame 
    global start_pb 
    global demo_frame 
    global question_desplayed_number_gui
    global total_score_weighted
    global total_score
    global time_x
    global questions_expected
    global question_and_sample_answer
    global question_and_how_to_answer
    global question_and_question_weight
    global question_and_worry_mental_state_weight
    global question_and_ambitious_mental_state_weight
    global question_and_greedy_mental_state_weight 
    global question_and_loyalty_mental_state_weight
    global question_and_vanity_mental_state_weight 
    global question_and_rouge_score_weight 
    global question_and_good_sample_answers
    global question_and_bad_answers
    global question_and_time_limit
    global Eval
    global qeval
    global Question_eval
    global toppart
    global bottompart
    global next_button
    global prev_button
    global question_gui
    question=qustion
    for widget in root.winfo_children():
        widget.destroy()
    time_y=time.time()-time_x
    if time_y < demo.time_limit[question_gu]:
        Time_score=0
    else:
        Time_score=0.05-(time_y*2/ demo.time_limit[question_gu])*0.01
    number_of_questions_gui=number_of_questions_gui-1
    demo.interview_interviewer_answer[qustion]=anser
    interviewee_answer=anser
    question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score=evaluation_of_single_answer_english(interviewee_answer,question_and_good_sample_answers[question],question_and_bad_answers[question],Time_score,question_and_rouge_score_weight[question],question_and_worry_mental_state_weight[question],question_and_ambitious_mental_state_weight[question],question_and_greedy_mental_state_weight[question],question_and_loyalty_mental_state_weight[question],question_and_vanity_mental_state_weight[question])
    feed_back_comments,gram_misses=feedback_evaluation(question_score,grammar_score,mistake_correction,time_score,rouge_score,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score)
    #the following line will be shown for each quesion at the final after ending the interview
    demo.evaluation_add(question,anser,question_score,gram_misses,feed_back_comments,worry_score,ambitious_score,greedy_score,loyalty_score,vanity_score,rouge_score,grammar_score,time_score)
    total_score_weighted=total_score_weighted+question_score * question_and_question_weight[question]
    total_score=total_score+question_score 
    if number_of_questions_gui == 0:
        Evaluation()
    else:
        enter_text_gui()
    

def guide_Tab():
    #guideline message is written her
    response = messagebox.showinfo("Guidelines", "Please wait 2 seconds after hearing the question to allow the program to detect the noise level /n /n The duration of each answer is fixed and suitable for each question \n \nPlease use headphons or external microphone for answering the question  \n \nIn case there is noise in your place and you can change your answer then submit  \n \n after clicking start recording wait to second then start to answer  \n \n when you start you will hear the question and you will see that the GUI (not responding) don't worry the application is just recording your answer")
    #Label(root, text= response).pack()
    
    
program_label=Label(root,text="DEMO INTERVIEW",padx = 20, pady = 20,font = ("Comic Sans MS", 26)).grid(row=0,column=0)    
guideline_btn = Button(root, text="GuideLines",padx = 10, pady = 20,font = ("Comic Sans MS", 12) ,command = guide_Tab).grid(row=1,column=0)    
start_pb=Button(root,text="start",padx=20,pady=20,font = ("Comic Sans MS", 12) ,command=enter_text_gui).grid(row=2,column=0)

root.mainloop()


# In[ ]:





# In[ ]:




