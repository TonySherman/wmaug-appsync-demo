import os

from aws_cdk import App, Environment

from services.merged_api.infrastructure.merged_api import MergedApiStack

app = App()

# Accounts
env = Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]
)

MergedApiStack(app, "merged-api-stack", env)

app.synth()
