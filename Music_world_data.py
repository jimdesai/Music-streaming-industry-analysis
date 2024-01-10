#Import required packages
import pandas as pd
import spotipy as spy
from spotipy.oauth2 import SpotifyClientCredentials as scc
""" ------------------------------------------------------ """
import csv
import itertools

#Authentication
class Authenticate(object):
    def _init_(self,cid,secret):
        if type(cid) & type(secret) == str: 
            self.cid = cid
            self.secret = secret
        else: raise ValueError('Not a string in Authenticate._init_')
    def spoauth(cid,secret):
        ccm =  scc(client_id=cid, client_secret=secret)
        sp = spy.Spotify(client_credentials_manager = ccm)
        return sp
    
class music_data(object):
    def _init_(self,uri):
        if type(uri) == str: self.uri = uri
        else: raise ValueError('Not a string in Playlist._init_')
    
    #Playlist info
    def playlist_data(sp,uri):
        tracks = pd.DataFrame()
        artists = pd.DataFrame()
        albums = pd.DataFrame()
        for x in sp.playlist_tracks(uri)["items"]:
            tracks = tracks._append(pd.DataFrame([x["track"]["name"]],columns=["Track"]))
            artists = artists._append(pd.DataFrame([x["track"]["artists"][0]["name"]],columns=["Artist"]))
            albums = albums._append(pd.DataFrame([x["track"]["album"]["name"]],columns=["Album"]))
        merged_data = pd.concat([tracks, artists, albums],axis=1)
        merged_data = merged_data.set_index('Track')
        return merged_data
    
    #Artist info
    def artist_data(sp,uri):
       main_artists = pd.DataFrame()
       popularity = pd.DataFrame()
       for x in sp.playlist_tracks(uri)["items"]:
           main_artists = main_artists._append(pd.DataFrame([x["track"]["artists"][0]["name"]],columns=["Main Artist"]))
           #secondary_artists = pd.DataFrame([x["track"]["artists"][1]["name"] for x in sp.playlist_tracks(uri)["items"]],columns=["Secondary Artist"])
           main_artists_uri = x["track"]["artists"][0]["uri"]
           popularity = popularity._append(pd.DataFrame([sp.artist(main_artists_uri)["popularity"]],columns=["Popularity"]))
       merged_data = pd.concat([main_artists,popularity],axis=1)
       merged_data = merged_data.set_index('Main Artist')
       return merged_data

    #Album info
    def album_data(sp,uri):
        album_name = pd.DataFrame()
        release_date = pd.DataFrame()
        for x in sp.playlist_tracks(uri)["items"]:
            album_name = album_name._append(pd.DataFrame([x["track"]["album"]["name"]],columns=["Album"]))
            release_date = release_date._append(pd.DataFrame([x["track"]["album"]["release_date"]],columns=["Release date"]))
        merged_data = pd.concat([album_name, release_date], axis=1)
        merged_data = merged_data.set_index('Album')
        return merged_data
    
    """ --------------------------------------------------------------------------------------------------------------------- """

    def Top_tracks_data(i,j,sp,artist_source_data):
        tracks = pd.DataFrame()
        popularity = pd.DataFrame()
        merged_data = pd.DataFrame()
        for row in artist_source_data.iloc[i:j,:].itertuples():
            for x in sp.artist_top_tracks(row.uri)["tracks"]:
                tracks = tracks._append(pd.DataFrame([x["name"]],columns=["Top tracks"]))
                popularity = popularity._append(pd.DataFrame([x["popularity"]],columns=["Popularity"]))
            data = pd.concat([tracks, popularity],axis=1)
            data['Artist'] = list(itertools.repeat(row.Artist, len(data)))
            merged_data = merged_data._append(data)
        merged_data = merged_data[['Artist','Top tracks','Popularity']].set_index('Artist')
        return merged_data
    
    def artist_genre_data(i,j,sp,artist_source_data):
        data = pd.DataFrame()
        merged_data = pd.DataFrame()
        for row in artist_source_data.iloc[i:j,:].itertuples():
            data = data._append(pd.DataFrame([x for x in sp.artist(row.uri)["genres"]],columns=['Genres'])).drop_duplicates()
            data['Artist'] = list(itertools.repeat(row.Artist, len(data)))
            merged_data = merged_data._append(data)
        merged_data = merged_data[['Artist','Genres']].set_index('Artist')
        return merged_data
    
    def artist_album_data(i,j,sp,artist_source_data):
        album_name = pd.DataFrame()
        release_date = pd.DataFrame()
        merged_data = pd.DataFrame()
        for row in artist_source_data.iloc[i:j,:].itertuples():
            for x in sp.artist_albums(row.uri)["items"]:
                album_name = album_name._append(pd.DataFrame([x["name"]],columns=["Albums"]))
                release_date = release_date._append(pd.DataFrame([x["release_date"]],columns=["Release date"]))
                data = pd.concat([album_name, release_date],axis=1)
                data['Artist'] = list(itertools.repeat(row.Artist, len(data)))
                merged_data = merged_data._append(data)
        merged_data = merged_data[['Artist','Albums','Release date']].set_index('Artist')
        return merged_data
    
    def album_market_data(sp,artist_source_data):
        data = pd.DataFrame()
        merged_data = pd.DataFrame()
        row = artist_source_data.iloc[0,:]
        for x in sp.artist_albums(row.uri)["items"]:
            merged_data = data._append(pd.DataFrame([y for y in x["available_markets"]],columns=['Available markets']))
            """ data['Albums'] = list(itertools.repeat(x["name"], len(data)))
            data['Artist'] = list(itertools.repeat(row.Artist, len(data)))
            merged_data = merged_data._append(data)
        merged_data = merged_data[['Artist','Albums','Available markets']].set_index('Artist') """
        return merged_data
    
    def artist_source_data(csv_file):
        with open(csv_file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader) 
            data = list(csv_reader)
            artist_source_data = pd.DataFrame()
            for row in data:
                artist_name = row[1]
                artist_username = row[2]
                spotify_link = row[3]
                uri = spotify_link.split("/")[-1].split("?")[0]
                artist_source_data = artist_source_data._append({'Artist':artist_name,'Username':artist_username, 'uri':uri},ignore_index=True)
        return artist_source_data
    
    def artist_album_datasave(xlsx_file):
        with pd.ExcelWriter(xlsx_file, mode="a") as writer:
            #artist_top_tracks_data.to_excel(writer, sheet_name="Top tracks data")
            artist_genre_data.to_excel(writer, sheet_name="Genre data")
            #artist_album_data.to_excel(writer, sheet_name="Albums data")
            #album_market_data.to_excel(writer, sheet_name="Market data")
            """ chunksize = len(album_market_data) // 1048576
            if len(album_market_data) % 1048576 > 0:
                chunksize += 1
            for i in range(0, len(album_market_data), chunksize):
                chunk = album_market_data.iloc[i:i + chunksize]
                chunk.to_excel(writer, sheet_name=f'Market data_{i+1}') """
        return None
   
#Assign the variables
cid = 'bb3fe30ef7b347799740701169250ab3'
secret = '124af749967843b1bcf2b117d9cb3ef0'
""" link = input("Playlist_link - ") """

#Process the data
""" uri = link.split("/")[-1].split("?")[0] """
sp = Authenticate.spoauth(cid, secret)
""" playlist_data = music_data.playlist_data(sp, uri)
artist_data = music_data.artist_data(sp,uri)
album_data = music_data.album_data(sp,uri) """
""" ------------------------------------------------- """
artist_source_data = music_data.artist_source_data('Artists data.csv')
#artist_top_tracks_data = music_data.Top_tracks_data(0,40,sp,artist_source_data)
artist_genre_data = music_data.artist_genre_data(0,40,sp,artist_source_data)
#artist_album_data = music_data.artist_album_data(0,40,sp,artist_source_data).drop_duplicates()
#album_market_data = music_data.album_market_data(sp,artist_source_data).drop_duplicates()

#Print the data
""" print(playlist_data.shape)
print(artist_data.shape)
print(album_data.shape) """
""" ------------------------- """
""" print(artist_top_tracks_data.shape)
print(artist_genre_data.shape)
print(artist_album_data.shape) """

#Save the data
music_data.artist_album_datasave("Artists data.xlsx")