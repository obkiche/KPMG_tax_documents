import pandas as pd
import numpy as np
import re
import spacy
import transformers


# Summarize one text

def summarize(text):
    
    # Removing the first common part

    splitted_text = text.split('Numac')
    splitted_text = splitted_text[1]

    # removing symbols

    no_symbols = splitted_text.replace('\n',' ')
    no_symbols = no_symbols.replace('/','')
    no_symbols = no_symbols.replace('§','')
    
    # Removing 'begin, eerste, laatste,...' from the end of the text and creating our main text.
    index = no_symbols.rfind('begin')
    
    corpus = no_symbols[:index]
    
    # Starting the summarizer
    
    import transformers
    undisputed_best_model = transformers.MBartForConditionalGeneration.from_pretrained(
        "ml6team/mbart-large-cc25-cnn-dailymail-nl-finetune")
    
    tokenizer = transformers.MBartTokenizer.from_pretrained("facebook/mbart-large-cc25")
    summarization_pipeline = transformers.pipeline(
        task="summarization",
        model=undisputed_best_model,
        tokenizer=tokenizer,
    )
    summarization_pipeline.model.config.decoder_start_token_id = tokenizer.lang_code_to_id[
        "nl_XX"
    ]


    article = corpus
    summary = summarization_pipeline(
        article,
        do_sample=True,
        top_p=0.75,
        top_k=50,
        # num_beams=4,
        min_length=50,
        early_stopping=True,
        truncation=True,
    )[0]["summary_text"]
    
    return summary


    '''--------------------------------------------------------------------------------------------------------'''

    # Looping through a .csv and creating summaries.

def summarize_csv(filepath):
    df = pd.read_csv(filepath)

    # Remove the German Translations

    df = df[df["Text"].str.contains("Duitse vertaling")==False]

    # Remove empty text rows if any are left.

    df.dropna(axis = 0, how ='any', inplace = True)
    
    # Create a summary column
    
    df['Summary'] = ''
    
    # Loop over the columns
    
    for idx, row in df.iterrows():
        
        text = df.loc[idx,'Text']
        
        # Removing the first common part

        splitted_text = text.split('Numac')
        splitted_text = splitted_text[1]

        # Removing symbols.

        no_symbols = splitted_text.replace('\n',' ')
        no_symbols = no_symbols.replace('/','')
        no_symbols = no_symbols.replace('§','')
    
        # Removing 'begin, eerste, laatste,...' from the end of the text and creating our main text.
        
        index = no_symbols.rfind('begin')
    
        corpus = no_symbols[:index]
    
        # loading mBart finetune Model

        undisputed_best_model = transformers.MBartForConditionalGeneration.from_pretrained(
            "ml6team/mbart-large-cc25-cnn-dailymail-nl-finetune"
        )
        tokenizer = transformers.MBartTokenizer.from_pretrained("facebook/mbart-large-cc25")
        summarization_pipeline = transformers.pipeline(
            task="summarization",
            model=undisputed_best_model,
            tokenizer=tokenizer,
        )
        summarization_pipeline.model.config.decoder_start_token_id = tokenizer.lang_code_to_id[
            "nl_XX"
        ]

        article = corpus 
        df.loc[idx,'Summary'] = summarization_pipeline(
            article,
            do_sample=True,
            top_p=0.75,
            top_k=50,
            # num_beams=4,
            min_length=50,
            early_stopping=True,
            truncation=True,
        )[0]["summary_text"]
        
    df = df.reset_index(drop=True)    
    df.to_excel("KPMG Tax Case - Summarized.xlsx", index=False)
    df.to_csv("KPMG Tax Case - CSV_Summarized.csv", index=False, encoding="utf-8-sig")