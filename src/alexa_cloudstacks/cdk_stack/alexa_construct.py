# For consistency with other languages, `cdk` is the preferred import name
from aws_cdk import core as cdk
from aws_cdk import (
    aws_iam,
    aws_lambda,
    aws_lambda_python,
    aws_logs,
)

from pathlib import Path


class AlexaConstruct(cdk.Construct):

    @property
    def function(self):
        return self._function

    def __init__(self, app: cdk.App, id: str, skill_id: str) -> None:
        super().__init__(app, id)

        # Skill lambda function
        self._function = aws_lambda_python.PythonFunction(
            scope=self,
            id='Lambda',
            entry='./src/alexa_cloudstacks/aws_lambdas/cloudstacks_skill',  # Path to function code
            description='Alexa Cloud Stacks Intents',
            environment=dict(
                POWERTOOLS_SERVICE_NAME=id,
                LOG_LEVEL='INFO',
            ),
            handler='handler',
            index='handler.py',
            log_retention=aws_logs.RetentionDays.ONE_WEEK,
            max_event_age=cdk.Duration.minutes(1),
            retry_attempts=0,
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            timeout=cdk.Duration.seconds(120),
            tracing=aws_lambda.Tracing.DISABLED,
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
