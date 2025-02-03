import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

environment = os.getenv("APP_ENV")

is_uat = environment == "uat"

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=is_uat, workers=4)
