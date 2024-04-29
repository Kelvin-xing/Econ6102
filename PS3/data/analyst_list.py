# -*- coding: utf-8 -*-

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
#from nltk.corpus import stopwords 
#from nltk.corpus import stopwords 
#from nltk.tokenize import word_tokenize 

import json
import csv

def load_csv(file_name):
    new_dict={}
    with open(file_name,"r",encoding='utf-8') as f:
        #reader=csv.reader(f)
        data=f.read()
        data1=data.split("\n")
        counter=0
        for line in data1:
            if line =="":
                continue
            line1=line.split(",")
            #print(line1)
            if counter==0:
                counter+=1
                continue
            else:
                counter+=1
                ticker=line1[1]
                year=line1[5]
                
                analyst_name=line1[7].lower()
                analyst_name_last = analyst_name.split(" ")[0]
                analyst_code=line1[6]
                company_name=line1[9].lower()
                company_code=line1[8]
                temp_dict={}
                temp_dict['analyst_name'] = analyst_name_last
                temp_dict['analyst_code'] = analyst_code
                temp_dict['company_name'] = company_name
                temp_dict['company_code'] = company_code
                temp_dict['ticker']=ticker
                temp_dict['year']=year
                #print(line1)
                #print(analyst_name_last)
                #print(company_name)
                if year+"|"+ticker not in new_dict.keys():
                    new_dict[year+"|"+ticker] = [temp_dict]
                else:
                    new_dict[year+"|"+ticker] += [temp_dict]
    f.close()
    return new_dict


new_dict=load_csv("Analyst List1.txt")

with open("analyst_json.txt","w+") as f:
    json.dump(new_dict, f)
