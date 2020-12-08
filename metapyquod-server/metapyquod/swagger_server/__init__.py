import os
from swagger_server.engine import Engine

mainEngine = Engine(os.environ["METAPYQUOD_IDX_TOML"])