import os

from aws_cdk import App, Environment

from services.inventory.infrastructure.inventory_stack import ProductInventoryStack


app = App()

env = Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])


ProductInventoryStack(app, "product-inventory-stack", env)

app.synth()
