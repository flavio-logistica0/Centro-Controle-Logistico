import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

HOST = os.getenv("DB_HOST", "localhost")
PORTA = os.getenv("DB_PORT", "5432")
BANCO = os.getenv("DB_NAME", "postgres")
USUARIO = os.getenv("DB_USER", "postgres")
SENHA = os.getenv("DB_PASSWORD")
