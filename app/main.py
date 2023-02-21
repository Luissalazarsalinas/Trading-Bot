from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import macd, mfi, sentiment_analysis


# Istance of the app
app = FastAPI()

# Add CORS 
# In this case i going to allow all origin for this API
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home path
app.get("/")
def home():
    return {
        "Message": "Stock Trading Strategy Api",
        "Health Check ": "OK",
        "Version": "0.0.1"
    }

# Add routers
app.include_router(macd.router)
# app.include_router(mfi.router)
app.include_router(sentiment_analysis.router)

#app.include_router(ml_strat.router)