import argparse, redis, shutil

parser = argparse.ArgumentParser(description='Export Redis database to a file')
parser.add_argument('--host', type=str, default='localhost', help='Redis host')
parser.add_argument('--port', type=int, default=6379, help='Redis port')
parser.add_argument('--file', type=str, required=True, help='File path to save the Redis data')

args = parser.parse_args()

r = redis.Redis(host=args.host, port=args.port)
r.save()

shutil.copyfile('/var/lib/redis/dump.rdb', args.file)