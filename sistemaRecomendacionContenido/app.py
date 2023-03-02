# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from srContenido import sisRec
from clasificadorPeliculas import cMovies
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oSisRec = sisRec()
oSisRec.obtenerDatos()
oSisRec.formatearDatos()
oCMovies = cMovies()


@app.get("/recomendar")
async def get_recomendacion():    
    response = oSisRec.obtenerRatingsUser()
    response = response.to_json(orient = 'records')    
    return response

@app.get("/similares/{movie_id}")
async def get_similares(movie_id: int):
    response = oCMovies.top_k_similares(movie_id,5)
    response = response.to_json(orient = 'records')    
    return response

@app.get("/user_movies/{user_id}")
async def get_user_movies(user_id: int):
    response = oSisRec.getUserMovies(user_id)
    response = response.to_json(orient = 'index')    
    return response 

@app.get("/user_profile")
async def get_user_profile():
    response = oSisRec.getUserProfileR()
    response = response.to_json()    
    return response