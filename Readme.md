# Music streaming industry analysis

## Project overview

The essence of this project is to gather some insights on the music industry streaming data specifically for the digital platform/application Spotify. About two aspects covered in the project are -
  1. Artists Performance
  2. Albums release strategy

## Data source

[Artist & Album dataset](https://github.com/jimdesai/Project1/blob/main/Artists%20%26%20Albums%20data.xlsx) - I have used this primary dataset containing detailed information on the top tracks data, albums release data and Artist-Fans engagement data of 40 most popular Indian music artists.

## Tools

  -  Python - Data extraction through web API as well as data transformation into machine readable format
  -  Tableau - Generating meaningful insights from data and creating a human understandable report

## Data extraction & transformation

Through the use Spotify web API and python, the following code was performed for the web scraping method of data extraction:

 ```python
 #Process the data
 sp = Authenticate.spoauth(cid, secret)
 artist_source_data = music_data.artist_source_data('Artists data.csv')
 artist_top_tracks_data = music_data.Top_tracks_data(0,40,sp,artist_source_data)
 artist_genre_data = music_data.artist_genre_data(0,40,sp,artist_source_data)
 artist_album_data = music_data.artist_album_data(0,40,sp,artist_source_data).drop_duplicates()
 album_market_data = music_data.album_market_data(sp,artist_source_data).drop_duplicates()

 #Save the data
 music_data.artist_album_datasave("Artists data.xlsx")
 ```
         
## EDA (Exploratory Data Analysis)

EDA involves exploring the Artist & Album dataset to answer some key questions such as -
  1. How much average popularity does the Indian artists share on the music streaming platform against the global music streaming industry?
  2. Aggregating the last ten years data, how much is the difference between the amount of album releases and an ideal Pareto 80/20 principle?
  3. In which regions of the world the albums are not released?
  4. When the topic is on artists interactions with the fans, which are the Indian artists known for strong positivity,enthusiasm and satisfaction among the fans?

## Data analysis

Here is an interactive tableau dashboard that I generated showing the answers of the EDA questions in a visual format.
  
[Download here](https://public.tableau.com/views/Project1_17048172258370/Story1?:language=en-US&:display_count=n&:origin=viz_share_link)

## References

1. [Introduction to computer science and programming](https://ocw.mit.edu/courses/6-00-introduction-to-computer-science-and-programming-fall-2008/download/)
2. Google Bard for understanding the EDA that can be performed in the music streaming industry
3. Basic to Advanced Tableau Dashboard Mastery Course by Jatan Shah
