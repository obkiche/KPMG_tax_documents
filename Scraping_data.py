# Importing modules

import pandas as pd
import numpy as np
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

#Opening the csv as a DataFrame and setting numerics as non-scientific.

df = pd.read_csv('KPMG Tax Case - Data Set.csv')
pd.set_option('display.float_format', lambda x: '%.f' % x)

# A check for empty cells and a warning for the user to rectify these.

if df.isna().sum().any():
    print('Warning, you have empty cells in the document, these will be removed. Please fill these in before applying this process ')
    print( 'These can be found in the following places rows: ', np.where(pd.isnull(df))[0], 'columns: ',np.where(pd.isnull(df))[1])

# rows with empty cells and duplicate rows are removed.    
df.dropna(axis = 0, how ='any', inplace = True)

df.drop_duplicates(subset = 'Link NL', keep= 'first', inplace = True)

# we change article to article_body in the hyperlink for better webscraping.

for idx , row in df.iterrows():
    
    substring = 'body'
    if substring not in df.loc[idx,'Link NL']:
        df.loc[idx,'Link NL'] = df.loc[idx,'Link NL'].replace('article','article_body')
    else:
        continue
    
    if substring not in df.loc[idx,'Link FR']:
        df.loc[idx,'Link FR'] = df.loc[idx,'Link FR'].replace('article','article_body')
    else:
        continue

# Decide on the webdriver to use.

driver = webdriver.Edge()

# Create an empty column

df['Text'] = " "

# Iterate over the rows

for idx , row in df.iterrows():
    #for link in df['Link NL']:
    
        # Get the url.
    url = df.loc[idx, 'Link NL']
    
        # Go to the website.
    driver.get(url)
    # time.sleep(random.uniform(1.0, 3.0))
    print(url)
    
        # For each url get the html body content and add them to the Text column.
    for element in driver.find_elements(By.TAG_NAME,"body"):
        text = element.text
        #text_list.append(text)
        df.at[idx,'Text'] = text
assert "No results found." not in driver.page_source
driver.close()

# Save it to excel

df.to_excel("KPMG Tax Case - Scraped Data.xlsx", index=False)




