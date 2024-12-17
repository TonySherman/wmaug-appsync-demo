import json
import boto3
from pydantic import BaseModel, Field, computed_field
from polyfactory.factories.pydantic_factory import ModelFactory
from faker import Faker
import random
import psycopg2
import psycopg2.extras


fake = Faker()


cf_client = boto3.client("cloudformation")
secrets_client = boto3.client('secretsmanager')


stacks = [
    "products-stack",
    "reviews-api-stack",
    "reviews-rds-stack",
    "product-inventory-stack",
]

exports = {}


for stack in stacks:
    response = cf_client.describe_stacks(StackName=stack)

    outputs = response["Stacks"][0].get("Outputs")

    if outputs:
        for output in outputs:
            exports[output["ExportName"]] = output["OutputValue"]

dynamodb = boto3.resource('dynamodb')

secret_string = secrets_client.get_secret_value(SecretId=exports["rds-secrets"])["SecretString"]
secret = json.loads(secret_string)

connection = psycopg2.connect(
    host="localhost", # localhost for portforwarded connection
    user=secret["username"],
    password=secret["password"],
    database=secret["dbname"],
    cursor_factory=psycopg2.extras.RealDictCursor,
    connect_timeout=10,
)

products_table = dynamodb.Table(exports['productsTableName'])
inventory_table = dynamodb.Table(exports['productsInventoryTableName'])

if not products_table and not inventory_table:
    raise


class Product(BaseModel):
    sku: str
    name: str
    description: str

    @computed_field
    @property
    def PK(self) -> str:
        return self.sku


class ProductCount(BaseModel):
    sku: str
    available_count: int = Field(gt=0, le=1000)

    @computed_field
    @property
    def PK(self) -> str:
        return self.sku

class ProductReview(BaseModel):
    sku: str
    rating: int = Field(gt=0, le=5)
    review: str
    author: str


class ProductFactory(ModelFactory[Product]): ...
class ProductCountFactory(ModelFactory[ProductCount]): ...
class ProductReviewFactory(ModelFactory[ProductReview]): ...

def create_review(sku: str):
    return ProductReviewFactory.build(sku=sku, author=fake.user_name(), review=fake.paragraph())

def write_review(review):
    with connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO product_reviews (sku, author, rating, review)
                VALUES (%s, %s, %s, %s)
                """,
                (review["sku"], review["author"], review["rating"], review["review"])
            )


for _ in range(1000):
    sku = fake.ean13()

    prefixes = ['Smart', 'Ultra', 'Pro', 'Elite', 'Quantum']
    suffixes = ['Pro', 'Max', 'Elite', 'Plus', 'Prime', 'X', 'Ultra']
    name = f'{random.choice(prefixes)} {fake.word().capitalize()} {random.choice(suffixes)}'

    product = ProductFactory.build(sku=sku, name=name, description=fake.sentence())
    product_count = ProductCountFactory.build(sku=sku)

    products_table.put_item(Item=product.model_dump())
    inventory_table.put_item(Item=product_count.model_dump())
    
    for _ in range(random.randint(1, 4)):
        review = create_review(sku).model_dump()
        write_review(review)
