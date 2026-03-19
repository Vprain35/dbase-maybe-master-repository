from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()

#going to website.com/number will now give them a random number (2 numbers, now)
@app.get("/number")
async def get_number():
    n1 = random.randint(0,12)
    n2 = random.randint(0,12)
    return {"n1":n1,"n2":n2}

@app.get("/product")
async def product(n1: int,n2: int):
    return n1*n2



app.mount("/", StaticFiles(directory="static", html=True), name="static")