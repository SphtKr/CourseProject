#!/usr/bin/env python3

import connexion

from swagger_server import encoder
from swagger_server import mainEngine

def main():
    options = {} #options = {"swagger_ui": False}
    
    app = connexion.App(__name__, specification_dir='./swagger/', options=options)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'MeTAPyquod Server'}, pythonic_params=True)
    app.run(server='gevent',port=8080)


if __name__ == '__main__':
    main()
