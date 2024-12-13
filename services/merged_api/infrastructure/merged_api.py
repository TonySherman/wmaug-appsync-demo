from aws_cdk import Environment, Stack, Tags, aws_appsync, aws_iam, aws_ssm
from constructs import Construct


class MergedApiStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        env: Environment,
    ) -> None:
        super().__init__(scope, id, env=env)

        Tags.of(self).add("project", "wmaug-dec-2024-appsync")

        merged_api_role = aws_iam.Role(
            self,
            "merged-api-execution-role",
            assumed_by=aws_iam.ServicePrincipal("appsync.amazonaws.com"),
            inline_policies={
                "execute_merged_api": aws_iam.PolicyDocument(
                    statements=[
                        aws_iam.PolicyStatement(
                            actions=[
                                "appsync:SourceGraphQL",
                                "appsync:StartSchemaMerge",
                                "lambda:InvokeFunction",
                            ],
                            resources=["*"],
                        ),
                    ]
                )
            },
        )

        aws_ssm.StringParameter(
            self,
            "merged_api_role_name",
            parameter_name="merged_api_role_name",
            string_value=merged_api_role.role_name,
        )

        merged_api = aws_appsync.GraphqlApi(
            self,
            "merged-api",
            name="merged_api",
            definition=aws_appsync.Definition.from_source_apis(source_apis=[], merged_api_execution_role=merged_api_role)
        )

        aws_ssm.StringParameter(
            self,
            "merged_api_id",
            parameter_name="merged_api_id",
            string_value=merged_api.api_id,
        )

    @staticmethod
    def add_source_api_to_merged_api(
        construct: Construct,
        api: aws_appsync.IGraphqlApi,
    ):
        return aws_appsync.SourceApiAssociation(
            construct,
            f"{construct.to_string()}-association",
            source_api=api,
            merged_api=aws_appsync.GraphqlApi.from_graphql_api_attributes(
                construct,
                "merged-api",
                graphql_api_id=aws_ssm.StringParameter.value_from_lookup(
                    construct, "merged_api_id"
                ),
            ),
            merged_api_execution_role=aws_iam.Role.from_role_name(
                construct,
                "merged_api_role",
                aws_ssm.StringParameter.value_from_lookup(
                    construct, "merged_api_role_name"
                ),
            ),
        )
