'''
Created on 2015-05-27

@author: legnain
'''
import functions as fun

if __name__ == '__main__':
    input_file = "emails.csv"
    daily_count_file = "domain.csv"
    output_file= "report.csv"
    
    daily_domain_list = fun.domains_extract(input_file)
    daily = fun.update(daily_domain_list, daily_count_file)
    fun.report30days(daily_count_file, output_file)
    print " The main file is working"