# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
from PyPDF2 import PdfReader, PdfFileWriter
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english')) 
#file_name = 'earning_call.txt'
embedding_path = 'glove.6B.50d.txt'
import json

infn = 'infn.pdf'
outfn = 'outfn.pdf'
# 获取一个 PdfReader 对象



def read_pdf(file_name):
    pdf_input = PdfReader(open(file_name, 'rb'))
    # 获取 PDF 的页数
    page_count = len(pdf_input.pages)
    print("page number", page_count)
    # 返回一个 PageObject
    page = pdf_input.pages[0]
    count=0
    page_content=""
    for page in pdf_input.pages:
        page_content += page.extract_text()
    return page_content
        #print(page_content+"\n")



#print(all_files)
def parsing_file_name(str_file):
    file_parsed=str_file.split(" ")
    company_name = file_parsed[0]
    year=file_parsed[1]
    quarter = file_parsed[2] 
    return company_name, year, quarter


##rewrite this session with regexpress matching...
##now we can match it with firm lists and analyst lists...
    
def eliminate_s(sentence, e_list):
    #rint("elist", e_list)
    #print(sentence)
    flag= 0
    while True:
        flag = -1
        for e in e_list:
            if e in sentence:
                flag=1
                loc_=sentence.find(e)
                sentence=sentence[0:loc_]+sentence[loc_+len(e):]
            else:
                pass
        if flag==-1:
            break
    return sentence

def reg_exp_matching(sentence,analyst_this_year_firm):
    #first from
    company=""
    Q_analyst=""
    analyst_list=[]
    analyst_company=[]
    for analyst_info in analyst_this_year_firm:
        if analyst_info['analyst_name']!='' and analyst_info['company_name'] !='':
            analyst_list += [analyst_info['analyst_name'].capitalize()]
            analyst_company +=[analyst_info['company_name'].capitalize()]
    special_company_list = ['J.P. Morgan', 'S.G. Cowen','Robert W. Baird', 'R.W. Baird', 'R. W. Baird','Stifel, Nicolaus']
    eliminate_sequence=[', please proceed', 'ahead', ', proceed', ', sir',' sir']
    reg_pair_head = [ "we have","we will go to","we will go first to","from the line of","line of", " from", "next to", "question for", "line to"]
    reg_pair_tail = ["representing", " with", " at", " from",",", " of"]
    for i in range(len(analyst_list)):
        analyst = analyst_list[i]
        sentence_list=sentence.split(' ')
        if analyst in sentence_list:
            #ok, we find it....
            #find first name...
            for j in range(len(sentence_list)):
                current_word=sentence_list[j]
                if current_word == analyst:
                    if j>0:
                        #find first name? - judege capital letter....
                        if sentence_list[j-1].lower().capitalize() == sentence_list[j-1]: 
                            Q_analyst = sentence_list[j-1]+" "+sentence_list[j]
                        else:
                            Q_analyst = analyst
                    else:
                        Q_analyst = analyst
                else:
                    pass
            company = analyst_company[i]
            print("1",company, Q_analyst)
            return company,Q_analyst
    #discard sequences in eliminate sequences
    #sentence_list=sentence.split(" ")
    #print("sentence", sentence, eliminate_sequence)
    sentence = eliminate_s(sentence, eliminate_sequence)

    
    for head in reg_pair_head:
        index0=sentence.find(head)
        if index0!=-1:
            sentence1 = sentence[index0+len(head):]
            for tail in reg_pair_tail:
                index1=sentence1.find(tail)
                if index1!=-1:
                    temp_list = sentence1[0:index1].split(" ")
                    if len(temp_list)>3:
                        #false finding...
                        continue
                    #find one...
                    if sentence1[0:index1]=="the line ":
                        continue
                    else:
                        Q_analyst = sentence1[0:index1]
                        ##get Q_analyst
                        for spe_company in special_company_list:
                            if spe_company in sentence:
                                company = spe_company
                                return company, Q_analyst
                        dot_pos = sentence1.find(".")
                        if dot_pos == len(sentence1)-1:
                            company = sentence1[index1+len(tail):-1]
                        elif dot_pos ==-1:
                            #not found dot
                            company = sentence1[index1+len(tail):-1]
                        else:
                            #not the last one, but find it...
                            #judge whether the next one is a space
                            if sentence1[dot_pos+1] !=" ":
                                #we are at the end of a sentence
                                company = sentence1[index1+len(tail)+1:dot_pos]
                            else:
                                #count forward until you find the first space...
                                #or perhaps next dot
                                for j in range((len(sentence1)-dot_pos)):
                                    if sentence1[j+dot_pos]==" ":
                                        break
                                company = sentence1[index1+len(tail)+1:(j+dot_pos)]
                else:
                    pass
                if company!="" or Q_analyst!="":
                    break
        else:
            pass
        if company!="" or Q_analyst!="":
            break
    #print("para is\n")
    #print(sentence)
    #print(company)
    #print(Q_analyst)
    if len(company.split(" "))>4 or len(Q_analyst.split(' '))>3:
        print("3")
        return '',''
    names =  Q_analyst.split(' ')
    if len(names)>0:
        last_name = names[-1]
        #check capitalization
        if last_name.lower().capitalize() != last_name:
            print("4",company, Q_analyst)
            return "",""
    print("2",company, Q_analyst)
    return company, Q_analyst


def parse_name_entity(sentence,analyst_info,company,year):
    #name entity recognition...
    #sentence_list = sentence.split(" ")
    #try:
    try:
        total_analysts_this_year_firm = analyst_info[year+"|"+company]
    except:
        total_analysts_this_year_firm = []
    company, name = reg_exp_matching(sentence,total_analysts_this_year_firm)            
    #name=""
    #company=""
    return name, company

#name, company = parse_name_entity("We'll go next to Paul Coster with J.P. Morgan.")
#print(name, company)
#print("extraction complete")





def para_extraction(paras,company,year):
    qa_list = []
    count_q = 0
    temp_dic = {}
    para_count=0
    temp_Q_name = ""
    temp_A_name = ""
    temp_Q_agency = ""
    #print("paras is\n", "\n||\n".join(paras))
    with open("analyst_json.txt","r") as f:
        analyst_info = json.load(f)
    
    for para in paras:
        if len(para) == 0:
            continue
        if para[0] != "<":
            if para_count==0:
                #extract name and agency
                temp_Q_name, temp_Q_agency  = parse_name_entity(para, analyst_info,company,year)
                para_count+=1
            else:
                #find nothing
                continue
        else:
            #print("para is\n", para)
            para_count+=1
            split = para.split('>:')
            if "A" in split[0]:
                session='A'
            elif "Q" in split[0]:
                session='Q'
            else:
                #no-session
                continue
            #session = split[0][-1]
            word_tokens = word_tokenize(split[-1].lower()) 
            #this is a list of words...
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            if session == 'Q':
                if count_q == 0:
                    #first time
                    temp_dic[session] = filtered_sentence
                    temp_dic["Q_company_name"] = temp_Q_agency
                    temp_dic["Q_analyst_name"] = temp_Q_name
                    temp_dic['A'] = []
                    temp_dic["Manager_name"] = []
                    count_q += 1
                else:
                    #print("temp_dic is\n", temp_dic)
                    if temp_dic["A"] != []:
                        #no answers...
                        qa_list.append(temp_dic)
                    temp_dic = {}
                    temp_dic["Q_company_name"] = temp_Q_agency
                    temp_dic["Q_analyst_name"] = temp_Q_name
                    temp_dic[session] = filtered_sentence
                    temp_dic['A'] = []
                    temp_dic["Manager_name"] = []
            if session == 'A':
                ##get A name...
                index0=split[0].find("-")
                if index0==-1:
                    temp_A_name=""
                else:
                    temp_A = split[0].split("-")
                    temp_A_name= temp_A[-1][1:-1]
                #print("current para is\n", para)
                if "A" not in temp_dic.keys():
                    #do nothing
                    #Q is not found yet...
                    continue
                else:
                    temp_dic['A'].append(filtered_sentence)
                    temp_dic["Manager_name"].append(temp_A_name)
    return qa_list



def clean_data(page_content):
    QA_sessions=page_content.split("Operator")
    para_list=[]
    for session in QA_sessions:
        if "<Q" not in session:
            continue
        session_paragraphs0=session.split("\n")
        temp_sessions=[]
        for para in session_paragraphs0:
            if ("Page" == para[0:4]) or (para==""):
                pass
            else:
                temp_sessions.append(para)
        session1=" ".join(temp_sessions)
        
        #session = session.replace("\n"," ")
        session_paragraphs = session1.split("<")
        all_paras=[]
        for para in session_paragraphs:
            if ">:" in para:
                all_paras.append("<"+para)
            else:
                all_paras.append(para)
        para_list.append(all_paras)
    return para_list

    #print(session)

# page_content=read_pdf("A 2004 Q4 Earnings Call.pdf")
# para_list = clean_data(page_content)

#print("\n||\n".join(para_list[0]))

#qa_list_all=[]
#for para in para_list:
#    for para in para_list:
 #       qa_list_temp = para_extraction(para)
  #      qa_list_all.append(qa_list_temp)
    
#print(qa_list_all[0])

#print(para_list)

##all files is the name of list

# 获取一个 PdfFileWriter 对象
#pdf_output = PdfFileWriter()
# 将一个 PageObject 加入到 PdfFileWriter 中
#pdf_output.addPage(page)
# 输出到文件中
#pdf_output.write(open(outfn, 'wb'))


def analyze_all():
    all_files=os.listdir()
    qa_list_all = []
    for file_name in all_files:
        ###establish a record
        qa_file ={}
        if ".pdf" not in file_name:
            continue
        print("now dealing with file", file_name)
        company, year, quarter = parsing_file_name(file_name)
        qa_file["company"]=company
        qa_file["year"]=year
        qa_file["quarter"]=quarter
        temp_content=read_pdf(file_name)
        para_list=clean_data(temp_content)
        qa_file_qas=[]
        for para in para_list:
            qa_list_temp = para_extraction(para,company,year)
            #print("para is\n\n", para)
            qa_file_qas.append(qa_list_temp)
        qa_file["QA_session"] = qa_file_qas
        qa_list_all.append(qa_file)
    return qa_list_all
        ####construct data/

qa_list_all = analyze_all()

#print(qa_list_all[0])
with open('qa_list_all.txt', 'w') as outfile:
    json.dump(qa_list_all, outfile)


