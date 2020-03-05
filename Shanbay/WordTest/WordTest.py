# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 11:03:53 2019

@author: YangYang
"""

import requests
import easygui as g
import xlwt

# 获取单词库链接和内容
def WordsWeb():
    title = "5分钟，评估你的单词量"
    msg = "评估过程包括三步：\n1. 选择适合你的出题范围\n2. 通过50个单词得到你的大致词汇量范围\n3. 检验你是否真的掌握你在第二步中选择的单词"
    choices  = ["GMAT", "考研", "高考", "四级", "六级", "英专", "托福", "GRE", "雅思", "任意"]    
    WordsRange = g.choicebox(msg, title, choices)
    RangeList = ['GMAT', '考研', '高考', '四级', '六级', '英专', '托福', 'GRE', '雅思', '任意']
    RangeWeb = ["GMAT", "NGEE", "NCEE", "CET4", "CET6", "TEM", "TOEFL", "GRE", "IELTS","NONE"]
    RangeDir = {key:value for key,value in zip(RangeList,RangeWeb)}
    Web = RangeDir[WordsRange]   
    postUrl = 'https://www.shanbay.com/api/v1/vocabtest/vocabularies/?category=' + Web
    r = requests.get(postUrl)
    WordsText = r.json()
    WordsList = WordsText['data']
    return WordsList

# 选择测试范围
def WordsListChoose():  
    WordsList = WordsWeb()
    WordsAll = [] 
    for word in WordsList:       
        content = word['content']
        WordsAll.append(content)
    title = "5分钟，评估你的单词量"
    msg = "请选择你认识的单词"
    choices  = WordsAll
    WordsChoose = g.multchoicebox(msg, title, choices)    
    return WordsChoose,WordsList

# 判断单词意思是否正确
def JudgeWords(word):
    WordsRight = []
    title = "5分钟，评估你的单词量"
    msg = word["content"]+"\n\n(可直接双击)"    
    choices = []
    WordsRight.append(word["content"])
    for i in range(4):
        choices.append(word["definition_choices"][i]["definition"])
        if word["definition_choices"][i]["pk"] == word["pk"]:
            WordsRight.append(word["definition_choices"][i]["definition"])
    choices.append("不认识")
    choose = g.choicebox(msg, title, choices=choices)    
    IsRight = (choose==WordsRight[1])  
    WordsRight.append(word["rank"])
    return IsRight, WordsRight

# 用户进行词意选择
def WordsMeaningChoose():
    WordsWrong = []
    WordsRank = []
    [WordsChoose,WordsList] = WordsListChoose()
    for i in range(len(WordsList)):
        if WordsList[i]["content"] in WordsChoose:
            [IsRight, WordsRight] = JudgeWords(WordsList[i])
            if IsRight:
                WordsRank.append(WordsRight[2])
            else:
                WordsWrong.append(WordsRight)
    if WordsRank == []:
        WordsNumber = 0
    else:
        WordsNumber = round(sum(WordsRank)/len(WordsRank))        
    return WordsNumber, WordsWrong, len(WordsChoose)

# 展示结果
def ShowResult():
    [WordsNumber, WordsWrong, TestNum] = WordsMeaningChoose()
    ShowWrong = "测试{}单词，其中正确单词{}个，错误单词{}个".format(TestNum, TestNum-len(WordsWrong), len(WordsWrong))
    WordsNumber = "单词量为{}".format(WordsNumber)
    ShowWrongWords = "\n"
    for i in range(len(WordsWrong)):
        ShowWrongWords = ShowWrongWords + ( "单词：{}，解释：{}".format(WordsWrong[i][0], WordsWrong[i][1])) + "\n"
    title = "5分钟，评估你的单词量"
    msg = ShowWrong + "\n" + WordsNumber +  "\n==========" + "\n以下单词需要学习哟" + ShowWrongWords
    choices  = ["保存错误单词", "直接退出"]
    IfSave = g.buttonbox(msg, title, choices=choices)
    if IfSave== "保存错误单词":
        SaveWords(WordsWrong)
        msg = "单词保存完毕，和程序在同一个文件夹下"
        g.msgbox(msg, title)

def SaveWords(WordsWrong):
    workbook = xlwt.Workbook()  #定义workbook
    sheet = workbook.add_sheet('单词')  #添加sheet
    head = [ '单词', '解释']
    for h in range(len(head)):
        sheet.write(0, h, head[h])    #把表头写到Excel里面去
    j = 1 #Excel开始写入的位置      
    for Word in WordsWrong:       
        sheet.write(j, 0, Word[0])
        sheet.write(j, 1, Word[1])
        j += 1    
    workbook.save("单词测试.xls")

if __name__ == "__main__":
    ShowResult()



