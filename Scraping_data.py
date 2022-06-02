import pandas as pd
import numpy as np

df = pd.read_csv('KPMG Tax Case - Data Set.csv')
pd.set_option('display.float_format', lambda x: '%.f' % x)

if df.isna().sum().any():
    print('Warning, you have empty cells in the document, these will be removed. Please fill these in before applying this process ')
    print( 'These can be found in the following places rows: ', np.where(pd.isnull(df))[0], 'columns: ',np.where(pd.isnull(df))[1])
    
df.dropna(axis = 0, how ='any', inplace = True)

df.drop_duplicates(subset = 'Link NL', keep= 'first', inplace = True)


for idx , row in df.iterrows():
    
    substring = 'body'
    if substring not in df.loc[idx,'Link NL']:
        df.loc[idx,'Link NL'] = df.loc[idx,'Link NL'].replace('article','article_body')
    else:
        continue
    

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By



driver = webdriver.Edge()
df['Text'] = " "

for idx , row in df.iterrows():
    #for link in df['Link NL']:
    
    url = df.loc[idx, 'Link NL']
    
    driver.get(url)
    # time.sleep(random.uniform(1.0, 3.0))
    print(url)
    for element in driver.find_elements(By.TAG_NAME,"body"):
        text = element.text
        #text_list.append(text)
        df.at[idx,'Text'] = text
assert "No results found." not in driver.page_source
driver.close()


df.to_excel("KPMG Tax Case - Scraped Data.xlsx", index=False)




