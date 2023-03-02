import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations

class cMovies():

    def __init__(self):
        self.pelis_movielens = pd.DataFrame()
        self.dicc_indice_movieid = {}
        self.dicc_movieid_indice = {}
        self.cosine_sims_ordenadas = None
        self.argumentos_bag_of_words = None
        self.orden_pelis_cosine_sims_por_fila = None
        self.obtenerDatos()
        self.init()

    def obtenerDatos(self):
        self.pelis_movielens = pd.read_csv("MovieLens_con_argumento.csv",sep=",")
        self.dicc_indice_movieid = self.pelis_movielens["movieId"].to_dict()
        self.dicc_movieid_indice = {valor: clave for clave, valor in self.dicc_indice_movieid.items()}

    #generar vectores
    def quitar_numeros(self,argumento):
        s = argumento.lower()
        s = re.sub(r"\d+", "", s)
        return s

    def tokenizador_generos(self,string_generos):
        generos_separados = string_generos.split("|")
        resultado = []
        for tamaño in [1,2]:
            combs = ["Géneros - " + "|".join(sorted(tupla)) for tupla in combinations(generos_separados, r=tamaño)]
            resultado = resultado + combs
        return sorted(resultado)

    def top_k_similares(self,movieId, k):
        fila_cosine_sims = self.dicc_movieid_indice[movieId]
        lista_ordenada_pelis_sim = self.orden_pelis_cosine_sims_por_fila[fila_cosine_sims]
        lista_ordenada_sim = self.cosine_sims_ordenadas[fila_cosine_sims]
        top_k = lista_ordenada_pelis_sim[:k]
        cosine_sims_top_k = lista_ordenada_sim[:k]
        top_k_df = self.pelis_movielens.loc[top_k].copy()
        top_k_df["similaridad"] = cosine_sims_top_k
        return top_k_df

    def init(self):
        contador_argumento = CountVectorizer(preprocessor = self.quitar_numeros, min_df = 5)
        argumentos_bag_of_words = (contador_argumento.fit_transform(self.pelis_movielens["argumento"]).toarray())

        columnas_argumentos = [tup[0] for tup in sorted(contador_argumento.vocabulary_.items(), key=lambda x: x[1])]
        argumentos_bag_of_words_df = pd.DataFrame(argumentos_bag_of_words, columns = columnas_argumentos, index=self.pelis_movielens["title"])

        contador_generos = CountVectorizer(tokenizer=self.tokenizador_generos, token_pattern=None, lowercase=False)
        contador_generos.fit(self.pelis_movielens["genres"])

        generos_bag_of_words = contador_generos.fit_transform(self.pelis_movielens["genres"]).toarray()

        columnas_generos = [tup[0] for tup in sorted(contador_generos.vocabulary_.items(),key=lambda x: x[1])]
        generos_bag_of_words_df = pd.DataFrame(generos_bag_of_words, columns= columnas_generos, index=self.pelis_movielens["title"])

        bag_of_words_ambos = np.hstack((argumentos_bag_of_words,generos_bag_of_words))
        bag_of_words_ambos_df = pd.DataFrame(bag_of_words_ambos,columns=columnas_argumentos+columnas_generos,index=self.pelis_movielens["title"])

        tf_idf = TfidfTransformer()
        tf_idf_pelis = tf_idf.fit_transform(bag_of_words_ambos_df).toarray()
        tf_idf_pelis_df = pd.DataFrame(tf_idf_pelis,columns=columnas_argumentos+columnas_generos,index=self.pelis_movielens["title"])

        cosine_sims = cosine_similarity(tf_idf_pelis_df)
        matriz_similaridades_df = pd.DataFrame(cosine_sims,columns=self.pelis_movielens["title"],index=self.pelis_movielens["title"])

        np.fill_diagonal(matriz_similaridades_df.values,np.nan)
        self.orden_pelis_cosine_sims_por_fila = np.argsort((-cosine_sims),axis=1)

        self.cosine_sims_ordenadas = np.sort(-cosine_sims,axis=1)

#print(dicc_indice_movieid )
#oCMovies = cMovies()

#res = oCMovies.top_k_similares(1,15)
#print(res)