import bs4
import requests
import csv
import re
import datetime
import os

league = ['ncaab', 'nba', 'mlb','nfl', 'ncaaf']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def date(month,nlist):
    global total, gdata
    if run == 3:
        total[0] = month + ' ' + gdata[nlist]

def teams(word):
    global gdata, run
    if gdata[1] == word:
        total[run] = gdata[0]
        date(word,2)
        gdata = gdata[2:]
    elif gdata[2] == word:
        total[run] = gdata[0] + ' ' + gdata[1]
        date(word,3)
        gdata = gdata[3:]
    elif gdata[3] == word:
        total[run] = gdata[0] + ' ' + gdata[1]  + ' ' + gdata[2]
        date(word,4)
        gdata = gdata[4:]
        
today = str((datetime.datetime.today()))
today = today.split(' ')
month = today[0]
month = month.split('-')
year = month[0]
month = int(month[1]) - 1
today = today[0]
print(today)
file_name = ["I:\\Coding Projects\\Sports Betting\\Projected Score\\Daily\\Games\\", year, " ", months[month], "\\",today, "\\"]
file_name = ''.join(file_name)
if not os.path.exists(file_name):
    os.makedirs(file_name)
name = file_name

for current in league:
    file_name = [name, current, " Projected Score.csv"]
    file_name = ''.join(file_name)
    link = 'https://www.oddsshark.com/' + current + '/computer-picks'
    sause = requests.get(link)
    soup = bs4.BeautifulSoup(sause.text, 'html.parser')
    for game in soup.find_all('table'):
        gdata = (game.text)
        gdata = re.split(' ', gdata)
        if gdata[0] == '':
            MD_T1 = gdata[1]
            gdata = gdata[2:]
            #Total = [Date, Team1, OS_Score1, Team2, OS_Score2, LV_Spread, LV_OU, MY_Team, MY_Spread]
            total = ['', '', '', '', '', '', '','','']
            run = 1
            teams('Matchup')
            run = 3
            MD_T2 = gdata[0]
            gdata = gdata[1:]
            teams('Dec')
            gdata = gdata[1:]
            total[2] = gdata[6][5:]
            total[4] = gdata[8][:4]
            if '.' not in total[4]:
                total[4] = total[4][:2]
            if '-' not in gdata[12]:
                total[5] = gdata[11] + ' ' + gdata[12]
            else:
                if gdata[11].startswith(MD_T1):
                    total[5] = MD_T2 + ' (+' + gdata[12][2:]
                else:
                    total[5] = MD_T1 + ' (+' + gdata[12][2:]
            total[6] = gdata[14][:-6]
            spread = total[5]
            spread = re.split(' ',spread)
            if spread[0].startswith(MD_T1):
                spread[1] = float(total[2]) + float(spread[1][2:-1]) - float(total[4])
            else:
                spread[1] = float(total[4]) + float(spread[1][2:-1]) - float(total[2])
            total[7] = spread[0]
            total[8] = spread[1]
            with open(file_name, 'a', newline='') as file:
                wr = csv.writer(file, dialect='excel')
                wr.writerow(total)
            print(total)


