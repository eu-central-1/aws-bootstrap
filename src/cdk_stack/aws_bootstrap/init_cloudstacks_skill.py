from pathlib import Path
from aws_cdk import (
    aws_iam,
    aws_lambda,
    core,
)

from aws_lambda_asset.zip_asset_code import ZipAssetCode


class AlexaConstruct(core.Construct):

    @property
    def function(self):
        return self._function

    def __init__(self, app: core.App, id: str, skill_id: str) -> None:
        super().__init__(app, id)
        work_dir = Path(__file__).parents[3]
        self._function = aws_lambda.Function(
            scope=self,
            id='cloudstacks_skill',
            code=ZipAssetCode(
                work_dir=work_dir,
                include=Path('src/lambdas/alexa_cloudstacks_skill'),
                file_name='.assets/alexa_cloudstacks_skill.zip'
            ),
            handler='handler.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            memory_size=1024,
            timeout=core.Duration.seconds(30)
        )

        self._function.add_to_role_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                resources=["*"],
                actions=["cloudformation:Describe*", "cloudformation:List*", "ec2:DescribeRegions"]
            )
        )

        self._function.add_permission(
            "1",
            principal=aws_iam.ServicePrincipal("alexa-appkit.amazon.com"),
            action="lambda:InvokeFunction",
            event_source_token=skill_id
        )
