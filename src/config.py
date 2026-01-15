from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field

class Settings(BaseSettings):
    # API Keys
    openai_api_key: SecretStr = Field(..., description="OpenAI API Key")
    tavily_api_key: SecretStr = Field(default=SecretStr(""), description="Tavily API Key (Optional)")

    # Model Configurations
    model_name: str = Field(default="gpt-4o", description="Main LLM Model Name")

    # Search Configurations
    max_search_results: int = Field(default=5, description="Max results for search tools")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
