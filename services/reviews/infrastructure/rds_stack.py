from aws_cdk import CfnOutput, Stack, aws_ec2, aws_iam, aws_rds, custom_resources, Tags
from constructs import Construct

from services.reviews.src.manage_database.infrastructure import ManageDatabaseLambda


class RdsStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        Tags.of(self).add("project", "wmaug-dec-2024-appsync")

        vpc = aws_ec2.Vpc(self, "aurora-vpc")

        self.rds_secrets = aws_rds.Credentials.from_generated_secret(
            username="rds_admin", secret_name="demo_rds_credentials"
        )

        rds_sg = aws_ec2.SecurityGroup(self, "rdsSg", vpc=vpc, allow_all_outbound=True)

        self.rds_cluster = aws_rds.DatabaseCluster(
            self,
            "postgres-cluster",
            vpc=vpc,
            security_groups=[rds_sg],
            default_database_name="demodb",
            engine=aws_rds.DatabaseClusterEngine.aurora_postgres(
                version=aws_rds.AuroraPostgresEngineVersion.VER_16_3
            ),
            credentials=self.rds_secrets,
            enable_data_api=True,
            serverless_v2_min_capacity=0,
            serverless_v2_max_capacity=4,
            writer=aws_rds.ClusterInstance.serverless_v2("writer"),
        )

        # database manager lambda to be used with CustomResource
        db_manager = ManageDatabaseLambda(
            self,
            "manage-database-lambda",
            vpc=vpc,
            rds_security_group=rds_sg,
            rds_secret_name=self.rds_secrets.secret_name,
        )

        # custom resource that invokes lambda on deploy
        # to help manage postgres instance
        custom_resources.AwsCustomResource(
            self,
            "rds-stack-custom-resource",
            on_update=custom_resources.AwsSdkCall(
                service="Lambda",
                action="invoke",
                parameters={
                    "FunctionName": db_manager.db_manager_lambda.function_name,
                    "InvocationType": "Event",
                },
                physical_resource_id=custom_resources.PhysicalResourceId.of(id)
            ),
            policy=custom_resources.AwsCustomResourcePolicy.from_statements(
                statements=[
                    aws_iam.PolicyStatement(
                        actions=["lambda:InvokeFunction"],
                        resources=[db_manager.db_manager_lambda.function_arn],
                    )
                ]
            ),
        )

        # This section is not necessary but does allow you to connect
        # to your RDS insance locally.
        #
        # It creates an ec2 instance that can connect to the RDS instance.
        #
        # Connect via aws session manager:
        #
        # aws ssm start-session \
        #     --document-name AWS-StartPortForwardingSessionToRemoteHost \
        #     --parameters '{"host":["<rds_host_endpoint>"], "portNumber":["5432"], "localPortNumber":["5432"]}' \
        #     --target <ec2 instance id>

        ec2_sg = aws_ec2.SecurityGroup(
            self,
            "ssm-security-group",
            vpc=vpc,
            allow_all_outbound=True,
        )

        ssm_instance = aws_ec2.Instance(
            self,
            "ssm_instance",
            instance_type=aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_ec2.MachineImage.latest_amazon_linux2023(),
            vpc=vpc,
            security_group=ec2_sg,
            ssm_session_permissions=True,
        )

        rds_sg.add_ingress_rule(
            connection=aws_ec2.Port.tcp(5432),
            peer=ec2_sg,
        )

        CfnOutput(self, "instance-id", value=ssm_instance.instance_id, export_name="ssm-instance-id")
        CfnOutput(self, "cluster-endpoint", value=self.rds_cluster.cluster_endpoint.hostname, export_name="rds-cluster-endpoint")
        CfnOutput(self, "rds-secrets", value=self.rds_secrets.secret_name, export_name="rds-secrets")

