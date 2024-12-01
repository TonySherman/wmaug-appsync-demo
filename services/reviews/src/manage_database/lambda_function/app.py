import json
import os
import urllib.request
import psycopg2
import psycopg2.extras


headers = {"X-Aws-Parameters-Secrets-Token": os.environ["AWS_SESSION_TOKEN"]}
secrets_extension_http_port = os.environ.get("PARAMETERS_SECRETS_EXTENSION_HTTP_PORT", "2773")
secrets_extension_endpoint = f"http://localhost:{secrets_extension_http_port}/secretsmanager/get?secretId={os.environ['PG_SECRETS_ARN']}"


def lambda_handler(event, context):
    req = urllib.request.Request(secrets_extension_endpoint, headers=headers)

    with urllib.request.urlopen(req) as response:
        response_text = response.read().decode("utf-8")

    secret_response = json.loads(response_text)
    secret = json.loads(secret_response['SecretString'])

    connection = psycopg2.connect(
        host=secret["host"],
        user=secret["username"],
        password=secret["password"],
        database=secret["dbname"],
        cursor_factory=psycopg2.extras.RealDictCursor,
        connect_timeout=10,
    )

    TABLE_CREATE_SQL = """
        CREATE TABLE IF NOT EXISTS
        product_reviews (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
            review_text TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(TABLE_CREATE_SQL)

    connection.close()
