import pathlib
from aws_cdk import Stack, aws_appsync, aws_dynamodb
import aws_cdk
from constructs import Construct

from services.merged_api.infrastructure.merged_api import MergedApiStack


class ProductsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        products_table = aws_dynamodb.Table(
            self,
            "products-table",
            partition_key=aws_dynamodb.Attribute(
                name="PK",
                type=aws_dynamodb.AttributeType.STRING,
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
        )

        aws_cdk.CfnOutput(self, "products_table_name", value=products_table.table_name, export_name="productsTableName")
        aws_cdk.CfnOutput(self, "products_table_arn", value=products_table.table_arn, export_name="productsTableArn")

        graph_api = aws_appsync.GraphqlApi(
            self,
            "products-api",
            name="products_api",
            definition=aws_appsync.Definition.from_file(f"{pathlib.Path(__file__).parent}/schema.graphql")
        )

        products_table_datasource = graph_api.add_dynamo_db_data_source(
            "products-table-data-source",
            table=products_table,
            name="products_dynamo_datasource"
        )


        graph_api.create_resolver(
            "product_resolver",
            type_name="Query",
            field_name="Product",
            data_source=products_table_datasource,
            runtime=aws_appsync.FunctionRuntime.JS_1_0_0,
            code=aws_appsync.Code.from_asset(f"{pathlib.Path(__file__).parent}/resolvers/product_resolver.js")
        )


        graph_api.create_resolver(
            "products_resolver",
            type_name="Query",
            field_name="Products",
            data_source=products_table_datasource,
            runtime=aws_appsync.FunctionRuntime.JS_1_0_0,
            code=aws_appsync.Code.from_asset(f"{pathlib.Path(__file__).parent}/resolvers/products_resolver.js")
        )

        MergedApiStack.add_source_api_to_merged_api(self, graph_api)

