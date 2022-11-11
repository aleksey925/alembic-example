from pathlib import Path

BASE_DIR = Path(__file__).absolute().parent

SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "app.db"}'
