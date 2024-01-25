import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy
review_list=[]

def get_soup(url):
    # İstek gönder
    response = requests.get(url)
    # HTML içeriğini analiz et
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_reviews(soup,film_name):
    #movie = soup.find('div',class_='parent')
    #movie_name = movie.find('a',)
    # Yorumları içeren bölümü seç
    reviews_section = soup.find('div', class_='lister-list')

    # Yorumları seç
    reviews = reviews_section.find_all('div', class_='review-container')
    for items in reviews:
        review={
            'movie_name':film_name,
            'title' :items.find('a', {'class':'title'}).text.strip(),
            #Bazı yorumlarda puanlama yok buna dikkat ederek tekrar gözden geçir
            #rating = review.find('span',{'class':'rating-other-user-rating'}).text.strip()
            'body' :items.find('div',{'class':'text show-more__control'}).text.strip(),
        }
        review_list.append(review)
        print(review['movie_name'],review['title'])
    
    
   
link_list=['https://www.imdb.com/title/tt0111161/reviews/?ref_=tt_ql_2','https://www.imdb.com/title/tt0068646/reviews/?ref_=tt_ql_2',
           'https://www.imdb.com/title/tt0468569/reviews/?ref_=tt_ov_rt','https://www.imdb.com/title/tt0071562/reviews/?ref_=tt_ov_rt',
           'https://www.imdb.com/title/tt0050083/reviews/?ref_=tt_ql_2','https://www.imdb.com/title/tt0108052/reviews/?ref_=tt_ql_2',
           'https://www.imdb.com/title/tt0167260/reviews/?ref_=tt_ql_2','https://www.imdb.com/title/tt0110912/reviews/?ref_=tt_ql_2',
           'https://www.imdb.com/title/tt0120737/reviews/?ref_=tt_ql_2','https://www.imdb.com/title/tt0060196/reviews/?ref_=tt_ql_2',
           'https://www.imdb.com/title/tt0109830/reviews/?ref_=tt_ql_2','https://www.imdb.com/title/tt0137523/reviews/?ref_=tt_ql_2',
           'https://www.imdb.com/title/tt0167261/reviews/?ref_=tt_ov_rt','https://www.imdb.com/title/tt1375666/reviews/?ref_=tt_ql_2',
           'https://www.imdb.com/title/tt0080684/reviews/?ref_=tt_ov_rt','https://www.imdb.com/title/tt0133093/reviews/?ref_=tt_ov_rt',
           'https://www.imdb.com/title/tt0099685/reviews/?ref_=tt_ov_rt','https://www.imdb.com/title/tt0073486/reviews/?ref_=tt_ov_rt',
           'https://www.imdb.com/title/tt0114369/reviews/?ref_=tt_ov_rt','https://www.imdb.com/title/tt0038650/reviews/?ref_=tt_ov_rt',
           'https://www.imdb.com/title/tt0047478/reviews/?ref_=tt_ov_rt','https://www.imdb.com/title/tt0816692/reviews/?ref_=tt_ov_rt',
           'https://www.imdb.com/title/tt0102926/reviews/?ref_=tt_ov_rt','https://www.imdb.com/title/tt0120815/reviews/?ref_=tt_ov_rt',
           'https://www.imdb.com/title/tt0317248/reviews/?ref_=tt_ov_rt']

movie_names=[" The Shawshank Redemption","The Godfather","The Dark Knight","The Godfather 2",
             "12 Angry Men"," Schindler's List","The Lord of the Rings: The Return of the King","Pulp Fiction",
             "The Lord of the Rings: The Fellowship of the Ring","Il buono, il brutto, il cattivo","Forrest Gump","Fight Club",
             "The Lord of the Rings: The Two Towers","Inception","Star Wars: Episode V - The Empire Strikes Back",
             "The Matrix","Goodfellas","One Flew Over the Cuckoo's Nest","Se7en","It's a Wonderful Life","Shichinin no samurai"," Interstellar",
             "The Silence of the Lambs"," Saving Private Ryan","Cidade de Deus"]

for link,movie_name in zip(link_list,movie_names):
    get_reviews(get_soup(link),movie_name)
    
df = pd.DataFrame(review_list)

df.to_excel('IMDBtop25.xlsx' , index=True,engine='openpyxl')

#cümlelere ayırma işlemi 
nlp = spacy.load('en_core_web_sm')

df = pd.read_excel('IMDBtop25.xlsx',engine='openpyxl')

def split_sentences(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    return sentences

df['body'] = df['body'].apply(lambda x :split_sentences(x) if pd.notna(x) else[])

df_expanded = df.explode('body').reset_index(drop=True)


df_expanded.to_excel('IMDBtop25_yorumlari(Ham-hali).xlsx',index=False,engine='openpyxl')

