import pathlib
from aws_cdk import Stack, aws_appsync, aws_rds, aws_secretsmanager
from constructs import Construct

from services.merged_api.infrastructure.merged_api import MergedApiStack


class ReviewsApiStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        cluster_id: str,
        rds_secret_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)


        rds_cluster = aws_rds.ServerlessCluster.from_serverless_cluster_attributes(
            self,
            "rds-cluster",
            cluster_identifier=cluster_id,
        )

        rds_secrets = aws_secretsmanager.Secret.from_secret_name_v2(
            self,
            "rds-secrets",
            secret_name=rds_secret_name,
        )

        graph_api = aws_appsync.GraphqlApi(
            self,
            "product-reviews-api",
            name="product_reviews_api",
            definition=aws_appsync.Definition.from_file(f"{pathlib.Path(__file__).parent}/schema.graphql")
        )

        graph_api.add_rds_data_source(
            "product-reviews-rds-datasource",
            rds_cluster,
            secret_store=rds_secrets,
        )

        MergedApiStack.add_source_api_to_merged_api(self, graph_api)
