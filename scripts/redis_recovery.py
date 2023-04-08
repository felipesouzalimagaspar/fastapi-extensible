import argparse, redis, shutil

parser = argparse.ArgumentParser(description='Export Redis database to a file')
parser.add_argument('--file', type=str, required=True, help='File path to save the Redis data')
args = parser.parse_args()

shutil.copyfile(args.file, '/var/lib/redis/dump.rdb')
