from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "lassodDB"
    SECRET_KEY: str = "jhdcvjhZDCygsdgfo7EW79ETE8GFYURFADUADF78rap9757p7349794tgirgfjhvdfjhvdcjxjvLZVse80r07q37r04r7-4r4rryegofuoefudvfyfyasdfvdyfvdyvfsyuvfusdfvy"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
