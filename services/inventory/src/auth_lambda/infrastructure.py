import pathlib
from aws_cdk import aws_lambda
from constructs import Construct


class AuthLambda(Construct):
    def __init__(
        self,
        scope: Construct,
        id: str,
    ) -> None:
        super().__init__(scope, id)

        self.auth_function = aws_lambda.Function(
            self,
            "authorizer-lambda",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=aws_lambda.AssetCode(
                f"{pathlib.Path(__file__).parent}/lambda_function"
            ),
            memory_size=512,
        )

