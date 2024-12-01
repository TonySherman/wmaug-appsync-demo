import os

from aws_cdk import App, Environment

app = App()

# Accounts
env = Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])

app.synth()

