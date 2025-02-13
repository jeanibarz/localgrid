from flask import Flask, jsonify
import psycopg2
import redis
import boto3
from grpc_client import say_hello
import os

app = Flask(__name__)

# Configuration (using environment variables or default values)
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'postgres')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'mydb')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

S3_ENDPOINT = os.environ.get('S3_ENDPOINT', 'http://localstack:4566')
S3_BUCKET = os.environ.get('S3_BUCKET', 'mybucket')

@app.route('/run')
def run_integration():
    results = {}

    # PostgreSQL test
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            port=POSTGRES_PORT
        )
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name TEXT);")
        cur.execute("INSERT INTO test (name) VALUES ('test name') RETURNING id;")
        inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.execute("SELECT name FROM test WHERE id = %s;", (inserted_id,))
        pg_result = cur.fetchone()[0]
        cur.close()
        conn.close()
        results['postgres'] = pg_result
    except Exception as e:
        results['postgres'] = str(e)

    # Redis test
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
        r.set('foo', 'bar')
        redis_result = r.get('foo').decode('utf-8')
        results['redis'] = redis_result
    except Exception as e:
        results['redis'] = str(e)

    # gRPC test
    try:
        grpc_result = say_hello("World")
        results['grpc'] = grpc_result
    except Exception as e:
        results['grpc'] = str(e)

    # S3 (LocalStack) test
    try:
        s3 = boto3.client('s3', endpoint_url=S3_ENDPOINT, region_name='us-east-1')
        # Create bucket (ignore error if it already exists)
        try:
            s3.create_bucket(Bucket=S3_BUCKET)
        except s3.exceptions.BucketAlreadyOwnedByYou:
            pass
        s3.put_object(Bucket=S3_BUCKET, Key='test.txt', Body=b'Hello S3')
        obj = s3.get_object(Bucket=S3_BUCKET, Key='test.txt')
        s3_result = obj['Body'].read().decode('utf-8')
        results['s3'] = s3_result
    except Exception as e:
        results['s3'] = str(e)

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
