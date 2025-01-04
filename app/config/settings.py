from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "RAG-QA"

    OPENAI_API_KEY: str

    CHROMA_PATH: str = "../data/chroma_data"
    FILE_STORE_PATH: str = "../data/files"

    MONGODB_CONNECTION_STRING: str = "mongodb://localhost:27017/"
    MONGODB_DATABASE: str = "rag_database"
    MONGODB_COLLECTION: str = "requests_data"

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", case_sensitive=False
    )


settings = Settings()
