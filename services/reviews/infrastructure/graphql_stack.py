import pathlib
from aws_cdk import Stack, aws_appsync, aws_rds, aws_secretsmanager, Tags
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

        Tags.of(self).add("project", "wmaug-dec-2024-appsync")

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

        rds_data_source = graph_api.add_rds_data_source(
            "product-reviews-rds-datasource",
            rds_cluster,
            secret_store=rds_secrets,
            database_name="demodb",
        )

        graph_api.create_resolver(
            "get_reviews_resolver",
            type_name="Query",
            field_name="getProductReviews",
            runtime=aws_appsync.FunctionRuntime.JS_1_0_0,
            code=aws_appsync.Code.from_asset(f"{pathlib.Path(__file__).parent}/resolvers/get_product_reviews.js"),
            data_source=rds_data_source,
        )

        MergedApiStack.add_source_api_to_merged_api(self, graph_api)
