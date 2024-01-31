# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 19:22:26 2018

@author: wobudong
"""

#爬取github中commits在1200次以上的人及commits分布情况

import requests
from bs4 import BeautifulSoup
import time
import random

startDate = ["xx","-01-01","-02-01","-03-01","-04-01","-05-01","-06-01","-07-01","-08-01","-09-01","-10-01","-11-01","-12-01"]
endDate = ["xx","-01-31","-02-28","-03-31","-04-30","-05-31","-06-30","-07-31","-08-31","-09-30","-10-31","-11-30","-12-31"]
#从一个比较知名用户"u2"开始爬取
url = "https://github.com/u2/"
#备选用户名列表
userList = ["u2"]
userListHead = 0
userListTail = 1
#符合条件用户数量
userDataNum = 0
#commits在1200次以上的用户列表
users = []
#存储commits在1200次以上的用户的文件名
usersFileName = "Users.txt"


#判断本条代理IP是否可用
def is_ok(socket):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)'
    }
    proxies = {
        'http': socket,
        'https': socket,
    }
    try:
        req=requests.get('http://httpbin.org/ip', headers=header, proxies=proxies)
        print('finish')
        print(req.text)
        return True
    except:
        print('no proxies')
        return False
        

#从国内代理IP网站爬取代理IP地址
#爬取20页 300条代理IP地址
def get_ip_pool():
    ipFile = open('IP.txt', 'w')
    for page in range(1,21,1):
        url = "https://www.kuaidaili.com/free/inha/" + str(page) + "/"
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        allTd = soup.find_all('td')
        socket = ""
        for td in allTd:
            data = td.get('data-title')
            if data == "IP":
                socket = td.text.replace('\xa0'*8,'\n\n')
            if data == "PORT":
                socket = socket + ":" + td.text.replace('\xa0'*8,'\n\n')
                ipFile.write(socket + '\n')
    ipFile.close()


#返回一个随机的请求头 headers
def get_headers():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent=random.choice(user_agent_list)
    headers = {'User-Agent': UserAgent}
    return headers


#返回一个随机的代理IP地址
def get_proxy():
    proxyFile = open('IP.txt', 'r')
    proxyList = proxyFile.readlines()
    for i in range(0, len(proxyList)):
        proxyList[i] = proxyList[i].rstrip('\n')
    proxy = random.choice(proxyList)
    #print(proxyList)
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    proxyFile.close()
    return proxies


#获取该用户关注者列表下的用户名,放进备选用户列表里，并返回队尾
def get_user_following(userFolloingUrl, userListTail):    
    req = requests.get(userFollowingUrl)
    html = req.text
    soup = BeautifulSoup(html,"lxml")
    userFollowings = soup.find_all('span', class_ = 'f4 link-gray-dark')
    for element in userFollowings:
        userName = element.text.replace('\xa0'*8,'\n\n') 
        if userName != "":
            userList.append(userName)
            userListTail = userListTail + 1
    return userListTail


#打印符合条件用户最近一星期(即2018.12.23-2018.12.29)的commits记录
def print_user_commits(userFileName):
    usersFile = open(userFileName, 'r')
    users = usersFile.readlines()
    for i in range(0, len(users)):
        users[i] = users[i].rstrip('\n')
    userDataNum = 0
    for userName in users:
        print("begin to print " + userName + "'s commits")
        fileName = "TXT/User" + str(userDataNum) + ".txt"
        myFile = open(fileName, 'w')
        myFile.write(userName+"\n")
        lastWeekCommitsUrl = "https://github.com/"+userName+"?tab=overview&from=2018-12-23&to=2018-12-29"
        req = requests.get(lastWeekCommitsUrl)
        html = req.text
        soup = BeautifulSoup(html,"lxml")
        lastWeekProjectCommits = soup.find_all('a', class_ = 'f6 muted-link ml-1')
        cnt = 0
        for commits in lastWeekProjectCommits:
            #获取项目名
            href = str(commits.get('href'))
            projectName = ""
            for letter in href:
                if letter != "?":
                    projectName = projectName + letter
                else: 
                    break
            projectName = projectName[:len(projectName)-7]
            
            #获取每个项目这周的commits信息
            detailedCommitUrl = "https://github.com"+projectName+"commits?author="+userName+"&since=2018-12-23&until=2018-12-30"
            time.sleep(int(random.uniform(2,4)))
            subReq = requests.get(detailedCommitUrl)
            subHtml = subReq.text
            subSoup = BeautifulSoup(subHtml,"lxml")
            relativeTime = subSoup.find_all('relative-time')
            #获取每一次提交的时间
            for element in relativeTime:
                datetime = str(element.get('datetime'))
                onePiece = str(cnt)+" "+projectName+" "+datetime
                print(onePiece)
                myFile.write(onePiece + '\n')
                cnt = cnt + 1  
        myFile.close()
        userDataNum = userDataNum + 1
        print("print " + userName + "'s commits successfully!\n")


get_ip_pool()

while userListHead < userListTail:
    usersFile = open("Users.txt", 'w')
    if userDataNum >= 20 :
        break
    userName = userList[userListHead]
    userListHead = userListHead + 1
    userFollowingUrl = "https://github.com/"+userName+"?tab=following"
    userListTail = get_user_following(userFollowingUrl, userListTail)
    time.sleep(int(random.uniform(2,4)))
    commitsNum = 0
    
    print("get user's following successfully")
   
    #遍历该用户最近七年每个月的commits记录
    for year in ["2018","2017","2016","2015","2014","2013","2012"]:
        for month in range(12,0,-1):
            eachMonthCommitsUrl = "https://github.com/"+userName+"?tab=overview&from="+year+startDate[month]+"&to="+year+endDate[month]
            
            #采用代理IP
            #while True:
            #    try:
            #        mainReq = requests.get(eachMonthCommitsUrl, headers=get_headers(), proxies=get_proxy())
            #    except:
            #        continue
            
            #不采用代理IP
            time.sleep(int(random.uniform(2,4)))
            mainReq = requests.get(eachMonthCommitsUrl)
            mainHtml = mainReq.text
            mainSoup = BeautifulSoup(mainHtml,"lxml")
            monthProjectCommits = mainSoup.find_all('a', class_ = 'f6 muted-link ml-1')
            #统计当月commits数量
            for element in monthProjectCommits:
                curNum = 0
                curCommitsNum = str(element.text.replace('\xa0'*8,'\n\n')) 
                for letter in curCommitsNum:
                    if letter >= "0" and letter <= "9":
                        curNum = curNum*10 + int(letter)
                    else:
                        continue
                commitsNum = commitsNum + curNum
            #简单剪枝
            if (commitsNum >= 1200) or (year == "2017" and curCommitsNum == 0):
                break
        if (commitsNum >= 1200) or (year == "2017" and curCommitsNum == 0):
                break
                           
    print("commitsNum is " + str(commitsNum))
    #找到一个符合条件用户存储起来
    if commitsNum >= 1200:    
        usersFile.write(userName+"\n")
        users.append(userName)
        userDataNum = userDataNum + 1
        usersFile.close()
print("Find 20 users!")

print("开始打印该20名用户2018.12.23-2018.12.29commits信息")
print_user_commits(usersFileName)    

