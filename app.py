from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import Recommenders as Recommenders
global s1,data
s1=0
data=0
rec_song=0
def model1(s1):
    song_df_1 = pd.read_csv('triplets_file.csv')
    song_df_1.head()
    song_df_2 = pd.read_csv('song_data.csv')
    song_df_2.head()
    song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on='song_id', how='left')
    song_df.head()
    print(len(song_df_1), len(song_df_2))
    len(song_df)
    song_df['song'] = song_df['title']+' - '+song_df['artist_name']
    song_df.head()
    song_df = song_df.head(20000)
    song_grouped = song_df.groupby(['song']).agg({'listen_count':'count'}).reset_index()
    song_grouped.head()
    grouped_sum = song_grouped['listen_count'].sum()
    song_grouped['percentage'] = (song_grouped['listen_count'] / grouped_sum ) * 100
    song_grouped.sort_values(['listen_count', 'song'], ascending=[0,1])
    ir = Recommenders.item_similarity_recommender_py()
    ir.create(song_df, 'user_id', 'song')
    user_items = ir.get_user_items(song_df['user_id'][10])
    for user_item in user_items:
        print(user_item)

    #ir.recommend(song_df['user_id'][300])


    df3=song_df[song_df['title'].str.contains(str(s1), na=False)][['song']]
    #df3
    list1=df3.values.tolist()
    #print(list1)
    t1=list1[0][0]
    #print(t1)

    ir.get_similar_items([str(t1)])
    global rec_song
    rec_song=Recommenders.df5
    #data=rec_song
    #print(data)
    #print(rec_song)  




app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')
    #return "<p>Hello, World!</p>"
@app.route("/",methods=['POST'])
def search():
    text=request.form['searchsong']
    s1=text
    model1(s1)
    print(rec_song)
    #xyz=['NAME', 'Alejandro - Lady GaGa', "Just Dance - Lady GaGa / Colby O'Donis", 'Creep (Explicit) - Radiohead', 'Love Story - Taylor Swift', 'Lucky (Album Version) - Jason Mraz & Colbie Caillat', 'Savior - Rise Against', 'Heartbreak Warfare - John Mayer', 'The Only Exception (Album Version) - Paramore', 'OMG - Usher featuring will.i.am', 'Bulletproof - La Roux']
    return render_template("recommend.html",data=rec_song)


if __name__=="__main__":
    app.run(debug=True)