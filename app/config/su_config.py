import os

from dotenv import load_dotenv

load_dotenv()


class SUConfig:
    SU_EMAIL = os.getenv("SU_EMAIL")
    SU_PHONE = os.getenv("SU_PHONE")
    SU_PASSWORD = os.getenv("SU_PASSWORD")
