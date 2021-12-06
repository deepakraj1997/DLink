from flask import Flask
from views.api import api
from config import config_dict

def main(init_db=True, debug=True, host='localhost'):
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix = '/api')
    app.config.update(**config_dict)
    print(app.config)
    app.run(debug = debug, host= host, port= app.config["server_port"])

if __name__ == "__main__":
    main()