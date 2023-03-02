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
        #Utilizando expresiones regulares para encontrar un año guardado entre paréntesis
        #Especificamos los paréntesis para no tener conflicto con las películas que tienen años como parte de su título
        self.df_movies['year'] = self.df_movies.title.str.extract('(\(\d\d\d\d\))',expand=False)
        #Eliminando los paréntesis
        self.df_movies['year'] = self.df_movies.year.str.extract('(\d\d\d\d)',expand=False)
        #Eliminando los años de la columna 'title'
        self.df_movies['title'] = self.df_movies.title.str.replace('(\(\d\d\d\d\))', '',regex=True)
        #Aplicando la función strip para eliminar los caracteres blancos finales
        self.df_movies['title'] = self.df_movies['title'].apply(lambda x: x.strip())    
        #Cada género está separado por un | para simplificar la llamada que se haga solo a |
        self.df_movies['genres'] = self.df_movies.genres.str.split('|')     
        #Copiando el marco de datos de la pelicula en uno nuevo ya que no necesitamos la información del género por ahora.
        self.df_movies_with_genres = self.df_movies.copy()
        #Para cada fila del marco de datos, iterar la lista de géneros y colocar un 1 en la columna que corresponda
        for index, row in self.df_movies.iterrows():
            for genre in row['genres']:
                self.df_movies_with_genres.at[index, genre] = 1
        #Completar los valores NaN con 0 para mostrar que una película no tiene el género de la columna
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
        #Eliminando información que no utilizaremos del dataframe de entrada
        inputMovies = inputMovies.drop(columns = 'genres').drop(columns = 'year')
        #Dataframe de entrada final        
        #Si una película que se agregó no se encuentra, entonces podría no estar en el dataframe 
        #original o podría estar escrito de otra forma, por favor revisar mayúscula o minúscula.
        #print(inputMovies)        
        #Descartando las películas de la entrada de datos
        self.userMovies = self.df_movies_with_genres[self.df_movies_with_genres['movie_id'].isin(inputMovies['movie_id'].tolist())]
        #print(userMovies)
        #Inicializando el índice para evitar problemas a futuro
        self.userMovies = self.userMovies.reset_index(drop=True)
        
        #Eliminando problemas innecesarios para ahorrar memoria y evitar conflictos
        userGenreTable = self.userMovies.drop(columns = 'movie_id').drop(columns = 'title').drop(columns = 'genres').drop(columns = 'year')
        #print(userGenreTable)
        #Producto escalar para obtener los pesos
        self.userProfile = userGenreTable.transpose().dot(inputMovies['rating'])
        #Perfil del usuario
        
        return self.userProfile

    def obtenerRatingsUser(self):                
        #Ahora llevemos los géneros de cada película al marco de datos original
        genreTable = self.df_movies_with_genres.set_index(self.df_movies_with_genres['movie_id'])
        #Y eliminemos información innecesaria
        genreTable = genreTable.drop(columns = 'movie_id').drop(columns = 'title').drop(columns = 'genres').drop(columns = 'year')
        #Multiplicando los géneros por los pesos para luego calcular el peso promedio
        recommendationTable_df = ((genreTable*self.userProfile).sum(axis=1))/(self.userProfile.sum())
        #print(recommendationTable_df.head())
        #Ordena nuestra recomendación en orden descendente
        recommendationTable_df = recommendationTable_df.sort_values(ascending=False)
        #Miremos los valores
        #print(recommendationTable_df)
        #recommendationTable_df.set_axis (['movie_id','rating'],axis='columns',inplace=True)
        #Tabla de recomendaciones final        
        recommendationMovieTable_df = self.df_movies[self.df_movies['movie_id'].isin(recommendationTable_df.head(10).keys())]        
        recommendationMovieTable_df = recommendationMovieTable_df.reset_index(drop=True)
        #print(recommendationMovieTable_df)
        recommendationMovieTable_df.genres = recommendationMovieTable_df.genres.apply(tuple)
        response_df = pd.merge(recommendationTable_df.to_frame(),recommendationMovieTable_df, on='movie_id')
        response_df.genres = response_df.genres.apply(list)
        #print(response_df[0])
        return response_df

#oSisRec = sisRec()
#oSisRec.obtenerDatos()
#oSisRec.formatearDatos()
#oSisRec.obteneRatingsUser(500)

