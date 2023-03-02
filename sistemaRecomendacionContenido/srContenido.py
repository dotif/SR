import numpy as np
import pandas as pd

class sisRec():
    def __init__(self):
        pd.set_option('display.max_columns', None)
        self.df_movies = pd.DataFrame()
        self.df_ratings = pd.DataFrame()
        self.df_users = pd.DataFrame()
        self.df_movies_with_genres = pd.DataFrame()
        self.userMovies = pd.DataFrame()
        self.um = pd.DataFrame()
        self.userProfile = None

    def obtenerDatos(self):
        columns_movies = ['movie_id', 'title', 'genres']    
        self.df_movies = pd.read_csv('movies.dat',sep='::', names=columns_movies, encoding = "latin", engine='python')    
        columns_ratings = ['user_id', 'movie_id', 'rating', 'timestamp']    
        self.df_ratings = pd.read_csv('ratings.dat',sep='::', names=columns_ratings, encoding = "latin", engine='python')
        columns_users = ['user_id', 'gender', 'age', 'occupation','zip_code']    
        self.df_users = pd.read_csv('users.dat',sep='::', names=columns_users, encoding = "latin", engine='python')
    
    def formatearDatos(self):
        
        self.df_movies['year'] = self.df_movies.title.str.extract('(\(\d\d\d\d\))',expand=False)
        #Eliminando los paréntesis
        self.df_movies['year'] = self.df_movies.year.str.extract('(\d\d\d\d)',expand=False)
        #Eliminando los años de la columna 'title'
        self.df_movies['title'] = self.df_movies.title.str.replace('(\(\d\d\d\d\))', '',regex=True)        
        self.df_movies['title'] = self.df_movies['title'].apply(lambda x: x.strip())            
        self.df_movies['genres'] = self.df_movies.genres.str.split('|')             
        self.df_movies_with_genres = self.df_movies.copy()
        
        for index, row in self.df_movies.iterrows():
            for genre in row['genres']:
                self.df_movies_with_genres.at[index, genre] = 1
        self.df_movies_with_genres = self.df_movies_with_genres.fillna(0)
        #print(self.df_movies_with_genres.head())

    def getUserMovies(self,user_id):
        self.getUserProfile(user_id)
        return self.um
    
    def getUserProfileR(self):
        return self.userProfile

    def getUserProfile(self,user_id):
        inputMovies = self.df_ratings.loc[self.df_ratings['user_id']==user_id]      
        #Filtrar las películas por título
        inputId = self.df_movies[self.df_movies['movie_id'].isin(inputMovies['movie_id'].tolist())]
        #Luego juntarlas para obtener el movieId. Implícitamente, lo está uniendo por título.
        inputMovies = pd.merge(inputId, inputMovies)
        self.um = inputMovies.copy(deep=True)
        
        inputMovies = inputMovies.drop(columns = 'genres').drop(columns = 'year')
        self.userMovies = self.df_movies_with_genres[self.df_movies_with_genres['movie_id'].isin(inputMovies['movie_id'].tolist())]
        self.userMovies = self.userMovies.reset_index(drop=True)                
        userGenreTable = self.userMovies.drop(columns = 'movie_id').drop(columns = 'title').drop(columns = 'genres').drop(columns = 'year')        
        self.userProfile = userGenreTable.transpose().dot(inputMovies['rating'])
                
        return self.userProfile

    def obtenerRatingsUser(self):                
        
        genreTable = self.df_movies_with_genres.set_index(self.df_movies_with_genres['movie_id'])
        genreTable = genreTable.drop(columns = 'movie_id').drop(columns = 'title').drop(columns = 'genres').drop(columns = 'year')        
        recommendationTable_df = ((genreTable*self.userProfile).sum(axis=1))/(self.userProfile.sum())        
        recommendationTable_df = recommendationTable_df.sort_values(ascending=False)        
        recommendationMovieTable_df = self.df_movies[self.df_movies['movie_id'].isin(recommendationTable_df.head(10).keys())]        
        recommendationMovieTable_df = recommendationMovieTable_df.reset_index(drop=True)        
        recommendationMovieTable_df.genres = recommendationMovieTable_df.genres.apply(tuple)
        response_df = pd.merge(recommendationTable_df.to_frame(),recommendationMovieTable_df, on='movie_id')
        response_df.genres = response_df.genres.apply(list)        
        return response_df

#oSisRec = sisRec()
#oSisRec.obtenerDatos()
#oSisRec.formatearDatos()
#oSisRec.obteneRatingsUser(500)

