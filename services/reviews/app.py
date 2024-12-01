import os

from aws_cdk import App, Environment

from services.reviews.infrastructure.graphql_stack import ReviewsApiStack
from services.reviews.infrastructure.rds_stack import RdsStack


app = App()

# Accounts
env = Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])

rds_stack = RdsStack(app, "reviews-rds-stack", env=env)

api = ReviewsApiStack(
    app,
    "reviews-api-stack",
    cluster_id=rds_stack.rds_cluster.cluster_identifier,
    rds_secret_name=rds_stack.rds_secrets.secret_name,
    env=env,
)


app.synth()
