import pandas as pd
import spacy 

nlp = spacy.load('en_core_web_sm')

df = pd.read_excel('IMDBtop25.xlsx',engine='openpyxl')

def split_sentences(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

df['body'] = df['body'].apply(lambda x :split_sentences(x) if pd.notna(x) else[])

df_expanded = df.explode('body').reset_index(drop=True)


df_expanded.to_excel('IMDBtop25_yorumlari(Ham-hali).xlsx',index=False,engine='openpyxl')

