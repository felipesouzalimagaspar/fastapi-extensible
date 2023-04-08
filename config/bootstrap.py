import yaml, os, redis, logging

def start_app():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(current_dir, "config.yml")
    with open(config_file, 'r') as stream:
        try:
            DATABASES = {}
            API = {}
            config = yaml.safe_load(stream)
            for db in config['app']['databases']:
                DATABASES[db['alias']] = redis.Redis(host=db['host'], port=db['port'], db=db['db'])
            API = config['app']['api']
            return DATABASES, API
        except yaml.YAMLError as e:
            print("Error on loading settings file:", e)

DATABASES, API = start_app()
request_logger = logging.getLogger('request_logger')
request_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logs/requests.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
request_logger.addHandler(file_handler)
