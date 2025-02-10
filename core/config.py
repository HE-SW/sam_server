from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Setting(BaseModel):
    port:int = int(os.getenv("PORT"))
    host:str = os.getenv("HOST")
    sam_model_path:str = os.getenv("SAM_MODEL_PATH")
    sam_model_type:str = os.getenv("SAM_MODEL_TYPE")
    sam_device:str = os.getenv("SAM_DEVICE")


config = Setting()