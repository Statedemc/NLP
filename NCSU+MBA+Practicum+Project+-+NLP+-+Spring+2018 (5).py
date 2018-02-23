
# coding: utf-8

# In[153]:


get_ipython().system('pip install nltk')
get_ipython().system('pip install PyPDF2')
get_ipython().system('pip install spacy')


# In[155]:


import nltk
import PyPDF2
import numpy


# In[ ]:


nltk.download()


# In[147]:


from nltk.tokenize import word_tokenize 
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag_sents
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import state_union
from io import StringIO
import io


# In[9]:


#set working directory for KB text file input
#useful link: https://www.youtube.com/watch?v=FLZvOKSCkxY&t=252s
import os
os.chdir("C:/Users/Patrick/Documents/MBA/MBA 545 - Practicum/NLP Python Project/KB Articles Source Files")


# In[43]:


#read file line by line into new file "next"
#this works.. but it appears the text file provides did not properly convert relevant sections hence e.g. "Cause" shows as blank
f = open("KB470899.txt")
next = f.readlines()
while next != "":
    print(next)
    next = f.readlines()


# In[105]:


#reading the resolution block only
#try regular expressions
#this works for text file
f = open("KB470899.txt", 'r')
data = f.read()
raw_file_extract = re.findall(r'Audience(.*?)Notes',data,re.DOTALL)
print(raw_file_extract)


# In[110]:


#write output to a file
#convert list to string to save to file
str1 = ''.join(raw_file_extract)
f = open('KB470899_StpWordsApplied.txt','w')
f.write(str1)
f.close()


# In[112]:


#Cleaning up Issue, Cause, Resolution Sections - Apply stop words
#using resulting "raw_file_extract", process stopwords and write into another file
import string 
with open('KB470899_StpWordsApplied.txt','r') as inFile, open('KB470899_StpWords_Done.txt','w') as outFile:
    for line in inFile.readlines():
        print(" ".join([word for word in line.lower().translate(str.maketrans('', '', string.punctuation)).split() 
                        if len(word) >=3 and word not in stopwords.words('english')]), file=outFile)


# In[165]:


# Sentence tokenization and pos-tagging
f = open("KB470899_StpWords_Done.txt") # using output file after applying stop words
raw_file=f.read()
sent_tokens = sent_tokenize(raw_file)

sent_tokens_str2 = ''.join(sent_tokens)
str_new = ("".join([s for s in sent_tokens_str2.splitlines(True) if s.strip()]))

f = open('KB470899_Sent_Tokens_Clean.txt','w')
f.write(str_new)
f.close()
print(str_new)


# In[141]:


# Word Tokenization
f = open("KB470899_Sent_Tokens.txt") # using output file from previous step
raw_file=f.read()
word_tokens = word_tokenize(raw_file)

def vertical_list():
    for i in word_tokens:
        print(i)

vertical_list() 


# In[151]:


#POS Tagging by looping over each sentence and tokenize it separately
f = open("KB470899_Sent_Tokens.txt") 
raw_file=f.read()
sentences = nltk.sent_tokenize(raw_file)   
 
data = []
for sent in sentences:
    data = data + nltk.pos_tag(nltk.word_tokenize(sent))

    # for word in data:
      #  if 'NN' in word[1]:
       #     print(word)
print(data)    


# In[ ]:


# APPROACH - NLP - NEXT STEPS:
# ===========================
# 1) Build a library based on Chao's rules with each keyword in one line
# 2) add code to match our tokenized words with dictionary keywords and record frequency
# 3) after running matching alg on all your words, apply weights/scores to each keyword or keywords to indicate 
# --- which most closely portend an iSCSI issue, cause or resolution or Notes signature
# 4) build a "signature" say "word1/word2/word3/word4" as our iSCSI signature for each section of the KB article
# 5) once we have a signature, you would need to be able to split your signature and add logic to search relevant
# --- KB articles to find which one's are indeed iSCSI issues
#  For config file --- 
# 6) we should be able to read the config file and check the file based on our rules where applicable e.g. does IP1 overlap IP2?
# --- IF YOU SEE THAT IN the config file, it suggests the customer has an iSCSI issue even though it's yet unreported


# In[176]:


#creating dictionary key-value pairs
import csv

with open('kb_dictionary_IssCauRes.csv', mode='r') as infile:
    reader = csv.reader(infile)
    #write to modified file with new k:v format
    with open('kb_dictionary_IssCauRes_new.csv', mode='w') as outfile: 
        writer = csv.writer(outfile)
        mydict = {rows[0]:rows[1] for rows in reader}
    print(mydict)


# In[202]:


# frequency for word_tokens
test_string = str_new
string_list = []
string_list = test_string.split()
wordfreq=[string_list.count(p) for p in string_list]
str6 = dict(zip(string_list,wordfreq))

#write to file
f = open('KB470899_Sent_Tokens_Freq.txt','w')
f.write(str(str6))
f.close()

print(dict(zip(string_list,wordfreq)))


# In[199]:


#function to order entries in dictionary
def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


# In[207]:


#sort word token by freq
sortFreqDict(str6)


# In[208]:


#write final freq. distribution to file
file = open('KB470899_Freq_Final.txt','w')
for index in range(len(string_list)): #,
    file.write(str(string_list[index]) + " " + str(wordfreq[index]) + "\n")
file.close()


# In[ ]:


# ***** I AM HERE **** Need to check this again
#Compare values in 'KB470899_Freq_Final.txt' to known dictionary based on DEMCs rules
for wordfreq, string_list in str6():
    first_word = key.split()[0]  # split on whitespace, take the first result
    if first_word in dict2: # this is our known keywords dictionary from DEMC
        dict2_value = dict2[first_word]
        print(dict1_value / dict2_value)

