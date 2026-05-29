from fastapi import FastAPI

app = FastAPI(title="Diccionario de pasillo API")


@app.get("/")
def root():
    return {"message": "Diccionario de pasillo API"}
