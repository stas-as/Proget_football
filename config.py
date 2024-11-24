from pydantic import model_validator, ConfigDict
from pydantic_settings import BaseSettings

class Setings(BaseSettings):
    PROXY_APYKEY: str
    class Config:
        env_file = ".env"
        
setings = Setings()
print(setings.PROXY_APYKEY)
