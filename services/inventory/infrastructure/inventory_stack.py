import pathlib
from aws_cdk import CfnOutput, Environment, Stack, aws_appsync, aws_dynamodb, Tags
import aws_cdk
from constructs import Construct

from services.inventory.src.auth_lambda.infrastructure import AuthLambda
from services.merged_api.infrastructure.merged_api import MergedApiStack


class ProductInventoryStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        env: Environment,
    ) -> None:
        super().__init__(scope, id, env=env)

        Tags.of(self).add("project", "wmaug-dec-2024-appsync")

        product_inventory_table = aws_dynamodb.Table(
            self,
            "product-inventory-table",
            partition_key=aws_dynamodb.Attribute(name="PK", type=aws_dynamodb.AttributeType.STRING),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
        )

        CfnOutput(self, "inventory_table_name", value=product_inventory_table.table_name, export_name="productsInventoryTableName")
        CfnOutput(self, "inventory_table_arn", value=product_inventory_table.table_arn, export_name="productsInventoryTableArn")

        graph_api = aws_appsync.GraphqlApi(
            self,
            "product-inventory-api",
            name="product_inventory_api",
            definition=aws_appsync.Definition.from_file(f"{pathlib.Path(__file__).parent}/schema.graphql")
        )

        product_inventory_table_datasource = graph_api.add_dynamo_db_data_source(
            "product-inventory-table-datasource",
            table=product_inventory_table
        )

        auth_lambda = AuthLambda(
            self,
            "auth-lambda",
        )

        lambda_datasource = graph_api.add_lambda_data_source(
            "auth-lambda-datasource",
            lambda_function=auth_lambda.auth_function,
        )

        auth_resolver_function = lambda_datasource.create_function(
            "auth-pipeline-function",
            name="auth_pipeline_function",
            code=aws_appsync.Code.from_asset(f"{pathlib.Path(__file__).parent}/resolvers/auth_function.js"),
            runtime=aws_appsync.FunctionRuntime.JS_1_0_0,
        )

        update_inventory_function = product_inventory_table_datasource.create_function(
            "update-inventory-function",
            name="update_inventory_function",
            code=aws_appsync.Code.from_asset(f"{pathlib.Path(__file__).parent}/resolvers/update_inventory.js"),
            runtime=aws_appsync.FunctionRuntime.JS_1_0_0,
        )

        graph_api.create_resolver(
            "product_inventory_resolver",
            type_name="Query",
            field_name="getInventory",
            data_source=product_inventory_table_datasource,
            runtime=aws_appsync.FunctionRuntime.JS_1_0_0,
            code=aws_appsync.Code.from_asset(f"{pathlib.Path(__file__).parent}/resolvers/get_product_inventory.js"),
        )

        graph_api.create_resolver(
            "update_product_inventory_resolver",
            type_name="Mutation",
            field_name="updateInventory",
            runtime=aws_appsync.FunctionRuntime.JS_1_0_0,
            code=aws_appsync.Code.from_asset(f"{pathlib.Path(__file__).parent}/resolvers/default.js"),
            pipeline_config=[
                auth_resolver_function,
                update_inventory_function,
            ],
        )
        

        MergedApiStack.add_source_api_to_merged_api(self, graph_api)
