import os
from dotenv import load_dotenv


load_dotenv()

HF_API_KEY = None

MODEL_NAME = "google/flan-t5-small"

FAISS_INDEX_PATH = "backend/db/faiss.index"