from django.shortcuts import render
from pymongo import MongoClient
import pandas as pd
from .spamfilter import predict
mongo=MongoClient("mongodb://localhost:27017/")
# Create your views here.
def login(request):
    return render(request,'login.html')

def homepage(request):
    if(request.method=="POST"):
        print(request.POST)
        findpass=mongo.flaskdb.mobologin.find({'usename':request.POST['username']})
        flag=0
        for j in findpass:
            if(j['usename']==request.POST['username']):
                flag=1
                passcheck=j['password']
        if(passcheck==request.POST['password']):
            return render(request,'homepage.html',{'prob':'0.89','val1':'FAIL','val2':'FAIL','val3':'FAIL'})
        return render(request,'login.html')

def checkspam(request):
    if(request.method=='POST'):
        print(request.POST)
        path="/home/aditya/Documents/sam_analyser/sam/files/"
        if(request.POST['inpfile']==''):
            path+='spam.txt'
        else:
            path+=request.POST['inpfile']
        level1='FAIL'
        level2='FAIL'
        level3='FAIL'
        file1=open(path,'r')
        filecontent=file1.read()
        import re
        matches=re.findall('@[a-z]*.',filecontent)
        match1=[]
        for i in matches:
            match1.append(i[1:len(i)-1])
        srframe=pd.read_csv('/home/aditya/Documents/sam_analyser/sam/files/searches.csv')
        recents=list(srframe['searches'])


        for j in match1:
            if(j in recents):
                level2='PASS'
                break
        print(level2)
        print(predict(filecontent))
        
        return render(request,'homepage.html',{'prob':'0.89','val1':level1,'val2':level2,'val3':level3})
        
    