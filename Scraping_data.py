# Importing modules

import pandas as pd
import numpy as np
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# This is the function to scrape a single url for text.

def scrape(url):
    
    # Decide on the webdriver to use.

    driver = webdriver.Edge()
    
    # URL compatibility check
    
    substring = 'body'
    
    if substring not in url:
        url = url.replace('article','article_body')
    print(url)
    
    # Go to the website

    driver.get(url)
    
    # Scrape the text from the website
    for elem in driver.find_elements(By.TAG_NAME,"body"):
        text = elem.text
         
    return text

'''---------------------------------------------------------------------------------------------------------------------------------------'''
# This is the function to scrape a website from the links in a .csv file.


def scrape_csv(filepath):
    df = pd.read_csv(filepath)
    pd.set_option('display.float_format', lambda x: '%.f' % x)

    # A check for empty cells and a warning for the user to rectify these.

    while df.isna().sum().any() >=1:
        
        print('Warning, you have empty cells in the document, these will be removed. Please fill these in before applying this process')
        print('These can be found in the following places rows: ', np.where(pd.isnull(df))[0], 'columns: ',np.where(pd.isnull(df))[1])
        print('Do you want to continue, yes/no? (Warning, typing yes will remove these rows!')

        cont = input("Continue? yes/no > ")

        while cont.lower() not in ("yes", "no"):
            cont = input("Not a valid answer, continue? yes/no > ")

        if cont == "no":
            print("Break")
            break
        
        if cont == 'yes':    
            # rows with empty cells are removed     
            df.dropna(axis = 0, how ='any', inplace = True)
            
            # Duplicate rows are removed.
            df.drop_duplicates(subset = 'Link NL', keep= 'first', inplace = True)

            # we change article to article_body in the hyperlink for better webscraping.
            substring = 'body'
            for idx , row in df.iterrows():
                if substring not in df.loc[idx,'Link NL']:
                    df.loc[idx,'Link NL'] = df.loc[idx,'Link NL'].replace('article','article_body')
                else:
                    continue
        
                if substring not in df.loc[idx,'Link FR']:
                    df.loc[idx,'Link FR'] = df.loc[idx,'Link FR'].replace('article','article_body')
                else:
                    continue
           # Create an empty column in the dataframe

            df['Text'] = " "   
    
            # Scraping part
        
            # Decide on the webdriver to use.

            driver = webdriver.Edge()
            
            # Iterate over the rows

            for idx , row in df.iterrows():
    
                # Get the url.
                url = df.loc[idx, 'Link NL']
    
                # Go to the website.
                driver.get(url)
                # time.sleep(random.uniform(1.0, 3.0))

    
                # For each url get the html body content and add them to the Text column.
            for element in driver.find_elements(By.TAG_NAME,"body"):
                text = element.text
                df.at[idx,'Text'] = text
            assert "No results found." not in driver.page_source
            driver.close()
    # Save it to excel and csv

    df.to_csv("KPMG_Scraped_Data.csv", index=False, encoding="utf-8-sig")