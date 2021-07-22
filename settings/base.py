from pathlib import Path

from environs import Env

env = Env()

ROLE = env.str('ROLE', default='local')
BASE_PATH = Path.cwd().absolute()
DEBUG = env.bool('DEBUG', default=True)
