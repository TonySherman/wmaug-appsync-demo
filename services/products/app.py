import os

from aws_cdk import App, Environment

from services.products.infrastructure.products_stack import ProductsStack

app = App()

env = Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])

ProductsStack(
    app,
    "products-stack",
    env=env,
)

app.synth()

