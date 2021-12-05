from bs4 import BeautifulSoup as bs
import lxml.html as lh
import requests
import numpy as np
import pandas as pd
import pdb


def scrape():
    #Base URL of what you want to scrape
    url='https://www.tenable.com/plugins/search?q=-_exists_%3Aagent+AND+script_name%3A%28websphere%29'

    #Get the contents of the website
    head_response = requests.get(url)

    #Store the HTML of the resposne and soupify it
    head_html = head_response.content
    head_soup = bs(head_html, 'lxml')

    #Get the number of pages you are looking for
    num_pages = head_soup.find('a', {'class': 'page-link page-text'}).get_text().split()[3]

    print(f'We found {num_pages} to scrape')

    #Get the results table
    head_results_table = head_soup.find('table', attrs={'class': 'results-table table'})

    #For each row, store each first element (header) and an empty list
    results_head = head_results_table.thead.find_all('tr')
    col = []
    for th in results_head[0].find_all('th'):
        col.append((th.text,[]))
    #print(col)

    #parse each result page for content
    page=1
    while page !=(int(num_pages)+1):
        #get the current page
        url=f'https://www.tenable.com/plugins/search?q=-_exists_%3Aagent+AND+script_name%3A%28websphere%29&sort=&page={page}'
        response = requests.get(url)
        html=response.content
        soup = bs(html, "lxml")
        results_table = soup.find('table', attrs={'class': 'results-table table'})
        
        #Get the table body
        tr_elements = results_table.tbody.find_all('tr')

        for j in  range(0,len(tr_elements)):
            #T is our j'th row
            T=tr_elements[j]

            #If row is not of size 7, the //tr data is not from our table 
            if len(T)!=7:
                break
            
            #n is the index of our column
            n=0
            
            #Iterate through each element of the row
            data = [ x.text for x in T ]
            print(f'Read {data}')

            with open('out.txt', 'a') as f:
                f.write(f'{",".join([ x.text for x in T ])}\n')

        #increment page
        page += 1

if __name__ == '__main__':
    with open('out.txt', 'w') as f:
        f.write(f'1,2,3,4,5,6,7\n')
    scrape()
