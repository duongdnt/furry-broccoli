import requests
from bs4 import BeautifulSoup
import re
from newspaper import Article
import csv
import time

#this is for time record
start_time = time.time()

#read the CSV file 
urls = []
with open ("data.csv", newline="", encoding="utf-8-sig") as file: 
    #create Reader object
    csv_reader = csv.reader(file, quoting = csv.QUOTE_NONE) 

    #turn each row into the string and append to urls list. 
    for row in csv_reader: 
        urls.append(''.join(row)) 

#loop through each url, and turn data into a dictionary with article name, author, email.
result = []; 
for url in urls: 
    #if there's no error, the dictionary will be appended to the result list
    try: 
        r = requests.get(url)
        mail_list=list(filter(lambda x: "sentry.io" not in x or ".png" not in x, re.findall("\w+@\w+\.{1}[a-zA-Z]+", r.text)))

        article = Article(url)
        article.download()
        article.parse() 

        row_dictionary = {
            "article_name": url, 
            "author": article.authors,
            "email": mail_list
        }
        result.append(row_dictionary)

    #if error happens, the dictionary will also be appended, but the author and email will tell something wrong with the link
    except: 
        row_dictionary = {
            "article_name": url, 
            "author": "error",
            "email": "error"
        }
        result.append(row_dictionary)
        continue

#after all the linked have been looped, the result will be written to the result.csv file
with open('result.csv', 'w',) as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['article_name', 'author', 'email'])
    for item in result:
        writer.writerow([item['article_name'],item['author'], item['email']])


#this is for time record
print("--- %s seconds ---" % (time.time() - start_time))
