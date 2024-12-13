import pathlib
import uuid
from aws_cdk import Duration, aws_ec2, aws_lambda, aws_secretsmanager
from constructs import Construct


class ManageDatabaseLambda(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
        vpc: aws_ec2.IVpc,
        rds_security_group: aws_ec2.ISecurityGroup,
        rds_secret_name: str,
    ) -> None:
        super().__init__(scope, id)

        lambda_security_group = aws_ec2.SecurityGroup(self, "lambda-sg", vpc=vpc)

        rds_security_group.add_ingress_rule(
            connection=aws_ec2.Port.tcp(5432), peer=lambda_security_group
        )

        rds_creds = aws_secretsmanager.Secret.from_secret_name_v2(
            self,
            "rds-secrets",
            secret_name=rds_secret_name,
        )

        secrets_layer = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            "secrets-layer",
            layer_version_arn="arn:aws:lambda:us-east-1:177933569100:layer:AWS-Parameters-and-Secrets-Lambda-Extension:12",
        )

        self.db_manager_lambda = aws_lambda.Function(
            self,
            "manage-database-lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=aws_lambda.AssetCode(
                f"{pathlib.Path(__file__).parent}/lambda_function"
            ),
            vpc=vpc,
            security_groups=[lambda_security_group],
            layers=[secrets_layer],
            # new function name forces custom resource invoke
            function_name=f"manage_db_{uuid.uuid4().hex[:8]}",
            environment={
                "PG_SECRETS_ARN": rds_creds.secret_arn,
                "PARAMETERS_SECRETS_EXTENSION_HTTP_PORT": "2773",
            },
            timeout=Duration.minutes(10),
            memory_size=1024,
        )

        rds_creds.grant_read(self.db_manager_lambda)
