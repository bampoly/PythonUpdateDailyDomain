'''
Created on 2015-05-27

@author: legnain
'''

import csv
import sqlite3
from datetime import *
from collections import *

def domains_extract(file_name):
# this function reads the .csv file that contain the daily Emails 
# then create a list of (day, domain, count) 
    daily = []
    date_and_domain = []
    Day_domain_count_ls = []
  
    with open(file_name, 'r') as f:
        file_content = csv.reader(f);                # store the content of csv file in file_content.
        for row in file_content:
            email = row[0].strip().lower()           # extract the email in lower-case letter without space.
            date  = row[1].strip()                   # extract the date
            date_and_domain.append([date, email[email.find('@')+1:]]) # extract the domain name from the email            
        d = [[i,date_and_domain.count(i)] for i in date_and_domain]   # count the emails

    # create a list of (day .... domain .... count)
    for element in d:
        if element not in Day_domain_count_ls:
            Day_domain_count_ls.append(element)  
            
    
    for v in Day_domain_count_ls:
        daily.append([v[0][0],v[0][1],v[1]])
    
    sorded_date = sorted(daily, key = lambda row: datetime.strptime(row[0], "%Y-%m-%d"))
        
    return  sorded_date


def update(daily_dom, daily_count_file):
# this function updates the database
    connetTo = sqlite3.connect("domains.db")
    c = connetTo.cursor() 
    c.execute("DROP TABLE IF EXISTS stocks")
    c.execute("CREATE TABLE stocks (day text, domain text, count int)")
    # Insert a row of data
    for v in daily_dom:
        c.execute("INSERT INTO stocks VALUES(?,?,?)",(v[0], v[1], v[2]))

    connetTo.commit()
    connetTo.close()
    
    write2csv(daily_dom, daily_count_file)  # append to the csv file

def write2csv(daily, daily_count_file):
    with open(daily_count_file, 'w+') as f:
        csv_writer = csv.writer(f)
        for v in daily:
            csv_writer.writerow([v[0], v[1], v[2]])
            
def report30days(daily_count_file,output_file):
# This function store a list of (date, domain, cummulative count). 
# The date sorted in ascending order. the formate of date is yyyy-mm-dd

# read data from csv file -----------------------------
    f = open(daily_count_file)
    data_in_file = csv.reader(f)
    date_domain_count = []
    for row in data_in_file: 
        date_domain_count.append(row)
    f.close()

# calculate the cumulative -----------------------------
# step 1   `
    #time_start = datetime.strptime(date_domain_count[0][0], "%Y-%m-%d").date()
    domain_count = defaultdict(list)
    cum_at_day = []
    for row in date_domain_count:
        domain_count[row[1]].append([row[0],row[2]])
     
# step 2
    today = date.today()
    period_of30days = today - timedelta(days=30)

    domain_cummulative = []
    increasing = 0
    for domain, count_per_day in domain_count.items():
        for i in  count_per_day:
            increasing = increasing + int(i[1])
            day_in_list = datetime.strptime(i[0], "%Y-%m-%d").date()
            if (day_in_list <= today and day_in_list >= period_of30days):
                domain_cummulative.append([i[0],domain , increasing])        
    sorded_date = sorted(domain_cummulative, key = lambda t: datetime.strptime(t[0], "%Y-%m-%d"))
    
    day0 = datetime.strptime(sorded_date[0][0], "%Y-%m-%d").date()   # this is the fisrt day in the list 
    day1 = datetime.strptime(sorded_date[-1][0], "%Y-%m-%d").date()  # this is the the recent day in the list
 
    temp = defaultdict(list)
    for day in sorded_date:
        dayC = datetime.strptime(day[0], "%Y-%m-%d").date()
        if (dayC == day0 or dayC == day1):
            temp[day[1]].append(float(day[2]))
            
    percentage = []        
    for v in temp.items():
        if  (len(v[1]) == 1): 
            percentage.append([v[0],0])
        else:
            percentage.append([v[0] ,100*(v[1][1] - v[1][0])/v[1][0]])
    
    perc_order = sorted(percentage, key = lambda t: t[1], reverse=True)

    with open(output_file, 'w+') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Date", "domain" , "growth %"])
        for v in perc_order:
            csv_writer.writerow([today, v[0], v[1]])