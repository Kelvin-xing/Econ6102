# -*- coding: utf-8 -*-

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import json
stop_words = set(stopwords.words('english')) 
file_name = 'earning_call.txt'
embedding_path = 'glove.6B.50d.txt'

# TODO: 去标点
def read_file(file_name):
    qa_list = []
    with open(file_name, 'r') as f:
        count_q = 0
        temp_dic = {}
        for line in f:
            if line[0] is not '<':
                continue
            split = line.split('>:')
            session = split[0][-1]
            word_tokens = word_tokenize(split[-1].lower()) 
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            if session == 'Q':
                if count_q == 0:
                    temp_dic[session] = filtered_sentence
                    temp_dic['A'] = []
                    count_q += 1
                else:
                    qa_list.append(temp_dic)
                    temp_dic = {}
                    temp_dic[session] = filtered_sentence
                    temp_dic['A'] = []
            if session == 'A':
                temp_dic[session].append(filtered_sentence)
    return qa_list

#qa = read_file(file_name)


#print("company is\n", qa_all[0]["company"],qa_all[0]["year"],qa_all[0]["quarter"])
#print("qa is\n",qa[0][0])

import numpy as np

def loadGloveModel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r',encoding='UTF-8')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.",len(model)," words loaded!")
    return model

glove = loadGloveModel(embedding_path)

from scipy.spatial.distance import cosine

def get_embedding(sentence, glove):
    length = len(sentence)
    embedding = 0
    for w in sentence:
        if w in glove:
            embedding += glove[w]
        else:
            length -= 1
    embedding /= length
    return embedding

def get_similarity(qas, glove):
    results = []
    for qa in qas:
        temp_res = []
        q_embedding = get_embedding(qa['Q'], glove)
        for a in qa['A']:
            a_embedding = get_embedding(a, glove)
            temp_res.append(cosine(q_embedding, a_embedding))
        results.append(temp_res)
    return results

def get_similarity1(qa, glove):
    #results = []
    temp_res = []
    try:
        q_embedding = get_embedding(qa['Q'], glove)
    except:
        return [0]
    for a in qa['A']:
        try:
            a_embedding = get_embedding(a, glove)
            temp_res.append(cosine(q_embedding, a_embedding))
        except:
            continue
    #results.append(temp_res)
    if temp_res==[]:
        return [0]
    return temp_res

def get_correlation_answer(qa, glove):
    answers = qa["A"]
    #cur_embedding = 0.0
    temp_res=[]
    sen_list=[]
    if len(answers)==1:
        n_answers=1
        para_cor=0
        count=0
        for a in qa["A"]:
            if a==[]:
                continue
            sen_temp = " ".join(a)
            sen_list+= sen_temp.split(".")
            #count=count+1
            #if count==1:
            #    a_embedding = get_embedding(a, glove)
                
            #else:
            #    cur_embedding=a_embedding
            #    a_embedding = get_embedding(a, glove)
            #    temp_res.append(cosine(cur_embedding, a_embedding))
    else:
        count=0
        for a in qa["A"]:
            if a==[]:
                continue
            sen_temp = " ".join(a)
            sen_list+= sen_temp.split(".")
            count=count+1
            if count==1:
                try:
                    a_embedding = get_embedding(a, glove)
                except:
                    continue
            else:
                try:
                    cur_embedding=a_embedding
                    a_embedding = get_embedding(a, glove)
                    temp_res.append(cosine(cur_embedding, a_embedding))
                except:
                    continue
        n_answers=len(answers)
        if temp_res==[]:
            para_cor = 0
        else:
            para_cor = np.mean(temp_res)
    #now compute for sen list...
    #print("sen_list is")
    #print(sen_list)
    sen_list1=[]
    for sen in sen_list:
        sen1=sen.split(" ")
        #print("sen1 is")
        #print(sen1)
        temp_sen=[]
        if len(sen1)==0:
            pass
        else:
            count_non_trivial=0
            for item in sen1:
                if item!="":
                    count_non_trivial+=1
                    temp_sen+=[item]
            if count_non_trivial ==0 :
                pass
            else:
                sen_list1 +=[temp_sen]
    sen_list=sen_list1
    count = 0
    if len(sen_list)==1:
        return 1,0,1,0
    temp_res_sen=[]
    for sen in sen_list:
        count=count+1
        if count == 1:
            new_sen = sen
        else:
            cur_sen=new_sen
            new_sen = sen
            #print("cur_sen", cur_sen)
            #print("new_sen", new_sen)
            if cur_sen == [] or cur_sen==[""]:
                continue
            if new_sen == [] or new_sen==[""]:
                continue
            try:
                cur_embedding = get_embedding(cur_sen, glove)
                new_embedding = get_embedding(new_sen, glove)
                temp_res_sen.append(cosine(cur_embedding, new_embedding))
            except:
                temp_res_sen.append(0)
    if temp_res_sen==[]:
        sen_cor=0
    else:
        sen_cor=np.mean(temp_res_sen)
    return n_answers, para_cor, len(sen_list1), sen_cor

#results = get_similarity(qa[0],glove)
#print(results)
    

def get_summary(qa):
    #results = []
    #temp_res = []
    #q_embedding = get_embedding(qa['Q'], glove)
    eff_q_words = len(qa['Q'])
    eff_a_words = 0
    n_sentence=0
    for a in qa['A']:
        #a_embedding = get_embedding(a, glove)
        #temp_res.append(cosine(q_embedding, a_embedding))
        eff_a_words+=len(a)
        sen = " ".join(a)
        n_sentence += len(sen.split("."))
    #results.append(temp_res)
    return eff_q_words,eff_a_words, n_sentence

    

def produce_all(qa_all,glove):
    file_str = "company\tyear\tquarter\tQ_company\tQ_analyst\tsession_number\tQA_similarity\tN_A_paragraphs\tsub_session_number\tManager_Name\tN_A_sentences\tN_A_para_corr\tN_A_sen_corr\tN_Q_words\tN_A_words\n".encode("utf-8")
    session_number = 0
    subsession_number = 0
    count_num=0
    for earning_report in qa_all:
        count_num+=1
        print("now deal with", count_num)
        temp_company = earning_report["company"]
        temp_year=earning_report["year"]
        temp_quarter=earning_report["quarter"]
        for qa in earning_report["QA_session"]:
            session_number+=1
            subsession_number = 0
            for session in qa:
                subsession_number+=1
                #this is a qa-session that contains multiple qas
                #we can get a list of paras
                #each session has multiple Q-A rounds...
                temp_Q_company = session["Q_company_name"]
                temp_Q_analyst = session["Q_analyst_name"]
                #temp_sentence_Q= session["Q"]
                #temp_sentence_list_A=session["A"]
                ##each round creates a record?
                #print("session is\n", session)
                result = get_similarity1(session,glove)
                if result == [0]:
                    continue
                record_temp = [temp_company, temp_year, temp_quarter, temp_Q_company, temp_Q_analyst,str(session_number)]
                #calculate the mean of QA...
                #subsession_number = 0
                #for sub_result in results:
                #subsession_number +=1
                mean_cor=np.mean(result)
                n_answers,n_cor, n_sentence, sen_cor=get_correlation_answer(session,glove)
                N_A_paragraphs = n_answers
                eff_q_words, eff_a_words, n_sentence1 = get_summary(session)
                    #I did not count number of words...
                try:
                    temp_manager = session["Manager_name"][0]
                except:
                    temp_manager = ""
                #print("Manager name is\n", session["Manager_name"])
                temp_new_result = "\t".join(record_temp)+"\t"+str(mean_cor)[0:4]+"\t"+str(N_A_paragraphs)+"\t"+str(subsession_number)+"\t"+temp_manager+"\t"+str(n_sentence)+"\t"+str(n_cor)+"\t"+str(sen_cor)+"\t"+str(eff_q_words)+"\t"+str(eff_a_words)+"\n"
                file_str = file_str+temp_new_result.encode("utf-8")
                #print("total file is\n")
                #print(file_str)
    #print(type(file_str))
    #print(len(file_str))
    file_str1=file_str.decode("utf-8")
    #print(type(file_str1))
    with open("result_table1.csv", "w", encoding="utf-8") as f:
        f.write(file_str1)
        f.close()
    print("file write complete\n")
    
with open("qa_list_all.txt","r") as f:
    qa_all=json.load(f)

#qa=qa_all[0]
#print(qa["company"])

produce_all(qa_all,glove)


