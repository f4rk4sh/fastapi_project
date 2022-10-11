from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class SUConfig(BaseSettings):
    SU_EMAIL: str
    SU_PHONE: str
    SU_PASSWORD: str


su_cfg = SUConfig()
