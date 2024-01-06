#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd


# In[ ]:


\\Users\\mahes\\Downloads\\movie_data\\movies.csv


# In[35]:


# What is the shape of "movies.csv"?
movie = pd.read_csv(r"C:\\Users\\mahes\\Downloads\\movie_data\\movies.csv")
movie.head()


# In[36]:


movie.shape


# In[37]:


#What is the shape of "ratings.csv"?
rating = pd.read_csv(r"C:\\Users\\mahes\\Downloads\\movie_data\\ratings.csv")


# In[7]:


rating.shape


# In[8]:


#How many unique "userId" are available in "ratings.csv"?
rating["userId"].nunique()


# In[9]:


# Which movie has recieved maximum number of user ratings?
rating


# In[10]:



mergedmov_rat= pd.merge( movie,rating, on = 'movieId')
mergedmov_rat.groupby('title')['rating'].count().sort_values(ascending=False).reset_index().head(1)


# In[38]:


tag = pd.read_csv(r"C:\\Users\\mahes\\Downloads\\movie_data\\tags.csv")
tag.head()


# In[12]:


#Select all the correct tags submitted by users to "Matrix, The (1999)" movie?
mergedmov_tags = pd.merge(movie, tag, on = "movieId")
mergedmov_tags[mergedmov_tags["title"]=="Matrix, The (1999)"]


# In[13]:


#What is the average user rating for movie named "Terminator 2: Judgment Day (1991)"?
mergedmov_rat[mergedmov_rat["title"]=="Terminator 2: Judgment Day (1991)"]["rating"].mean()


# In[14]:


import seaborn as sns


# In[15]:


#How does the data distribution of user ratings for "Fight Club (1999)" movie looks like?
Fight_rat = mergedmov_rat[mergedmov_rat["title"]=="Fight Club (1999)"]["rating"]
sns.kdeplot(Fight_rat)


# From above plot the fight club rating is  Left Skewed Distribution

# In[16]:


#1. Group the user ratings based on movieId and apply aggregation operations like count and mean on ratings.
mergedmov_rat= pd.merge( movie,rating, on = 'movieId')
mergedmov_rat["rating"].count()


# In[17]:


mergedmov_rat["rating"].mean()


# In[18]:


#1. Group the user ratings based on movieId and apply aggregation operations like count and mean on ratings.

grouped_ratings = rating.groupby('movieId').agg({'rating': ['count', 'mean']}).reset_index()
grouped_ratings


# In[19]:


grouped_ratings.columns = ['movieId', 'rating_count', 'rating_mean']


# In[20]:


#2. Apply inner join on dataframe created from movies.csv and the grouped df from step 1.
merged_df = pd.merge(movie, grouped_ratings, on='movieId', how='inner')


# In[21]:


#3. Filter only those movies which have more than 50 user ratings (i.e. > 50).

filtered_movies = merged_df[merged_df['rating_count'] > 50]


# In[22]:


filtered_movies


# In[23]:


#Which movie is the most popular based on  average user ratings?
filtered_movies.sort_values(by="rating_mean",ascending=False).head()


# In[24]:


#Select all the correct options which comes under top 5 popular movies based on number of user ratings.
filtered_movies.sort_values(by="rating_count",ascending=False).head()


# In[25]:


#Which Sci-Fi movie is "third most popular" based on the number of user ratings?
filtered_movies[filtered_movies['genres'].apply(lambda x: 'Sci-Fi' in x.split('|'))].sort_values(by='rating_count',ascending=False)


# In[39]:


link = pd.read_csv(r"C:\\Users\\mahes\\Downloads\\movie_data\\links.csv")


# In[27]:


link


# In[ ]:





# ### Using "links.csv", scrape the IMDB reviews of each movie with more than 50 user ratings. "README.md" file contains the required details.

# In[29]:


import numpy as np
from bs4 import BeautifulSoup
movies_with_imdb_ids = pd.merge(filtered_movies, link, on='movieId', how='inner')

# Function to scrape IMDB reviews for a movie given its IMDB ID
def scrapper(imdb_id):
    id_str = str(int(imdb_id))
    n_zeroes = 7 - len(id_str)
    new_id = "0" * n_zeroes + id_str
    URL = f"https://www.imdb.com/title/tt{new_id}/reviews"
    request_header = {
        'Content-Type': 'text/html; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    response = requests.get(URL, headers=request_header)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all review containers
    review_containers = soup.find_all('div', class_='text show-more__control')  # Update this class to the actual review container class
    
    reviews = [container.text.strip() for container in review_containers]
    return reviews

# Iterate through movies with IMDB IDs and scrape reviews
reviews_data = []
for index, row in movies_with_imdb_ids.iterrows():
    imdb_id = row['imdbId']
    movie_reviews = scrapper(imdb_id)
    reviews_data.extend([(imdb_id, review) for review in movie_reviews])

# Create a DataFrame from the collected reviews
reviews_df = pd.DataFrame(reviews_data, columns=['imdbId', 'Review_Text'])


# In[30]:


reviews_df.to_csv("reviews.csv")


# In[31]:


reviews_df


# In[32]:


movie


# In[34]:


merged_reviews_links = pd.merge(reviews_df, link, on='imdbId', how='inner')

merged_reviews_links_ratings = pd.merge(merged_reviews_links,filtered_movies, on = 'movieId', how = 'inner')


# In[35]:


#Mention the movieId of the movie which has the highest IMDB rating

merged_reviews_links_ratings.sort_values(by='rating_count',ascending=False)


# In[36]:


#Mention the movieId of the "Sci-Fi" movie which has the highest IMDB rating.
merged_reviews_links_ratings[merged_reviews_links_ratings['genres'].apply(lambda x: 'Sci-Fi' in x.split('|'))].sort_values(by='rating_count',ascending=False)

