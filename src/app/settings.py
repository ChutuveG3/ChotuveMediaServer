# settings.py
from dotenv import load_dotenv
from pathlib import Path  # python3 only
from version import Version
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
