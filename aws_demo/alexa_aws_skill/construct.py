from aws_cdk import (
    Duration,
    aws_iam,
    alexa_ask,
    aws_s3_assets,
    # aws_kms,
    aws_lambda,
    aws_lambda_python_alpha as aws_lambda_python,
    aws_logs,
)
from constructs import Construct


class AlexaConstruct(Construct):

    @property
    def function(self):
        return self._function

    def __init__(self, scope: Construct, id: str, skill_id: str) -> None:
        super().__init__(scope, id)

        # Install ASK cli and run 'ask configure'
        # Then read carefully following link
        # noqa https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-authenticationconfiguration.html
        # Finally add your LWA credeentials to ~/.cdk.json file
        # {
        #   "context": {
        #     "amazon-developer-smapi:vendor-id": "your-vendor-id",
        #     "amazon-developer-smapi:client-id": "amzn1.application-oa2-client.123",
        #     "amazon-developer-smapi:client-secret": "abc",
        #     "amazon-developer-smapi:refresh-token": "ABC"
        #   }
        # }
        self._skillauth = alexa_ask.CfnSkill.AuthenticationConfigurationProperty(
            client_id=self.node.try_get_context('amazon-developer-smapi:client-id'),
            client_secret=self.node.try_get_context('amazon-developer-smapi:client-secret'),
            refresh_token=self.node.try_get_context('amazon-developer-smapi:refresh-token')
        )

        self._skillassetrole = aws_iam.Role(
            scope=self,
            id='SkillAssetRole',
            assumed_by=aws_iam.CompositePrincipal(
                aws_iam.ServicePrincipal('alexa-appkit.amazon.com'),
                aws_iam.ServicePrincipal('cloudformation.amazonaws.com')
            )
        )

        self._skillasset = aws_s3_assets.Asset(
            scope=self,
            id='SkillAsset',
            path='./aws_demo/alexa_aws_skill/assets/skill',
            readers=[self._skillassetrole]
        )

        self._skillassetrole.add_to_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=[
                    'kms:Decrypt',
                    'kms:DescribeKey',
                ],
                resources=['*'],
                #  resources=[aws_kms.Alias.from_alias_name(scope=self,
                #                                           id='SkillAssetKmsAlias',
                #                                           alias_name='alias/aws/s3').key_arn],
            )
        )

        # Skill lambda function
        self._function = aws_lambda_python.PythonFunction(
            scope=self,
            id='Lambda',
            entry='./aws_demo/alexa_aws_skill/assets/lambda',  # Path to function code
            description='Alexa AWS Command Intents',
            # bundling=dict(
            #     environment=dict(
            #         POETRY_VIRTUALENVS_IN_PROJECT= True,
            #     ),
            # ),
            environment=dict(
                POWERTOOLS_SERVICE_NAME=id,
                LOG_LEVEL='INFO',
            ),
            handler='handler',
            index='handler.py',
            log_retention=aws_logs.RetentionDays.ONE_WEEK,
            max_event_age=Duration.minutes(1),
            retry_attempts=0,
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            memory_size=1024,
            timeout=Duration.seconds(120),
            tracing=aws_lambda.Tracing.DISABLED,
        )

        self._function.add_to_role_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                resources=["*"],
                actions=["cloudformation:Describe*", "cloudformation:List*", "ec2:DescribeRegions"]
            )
        )

        self._skillpackage = alexa_ask.CfnSkill.SkillPackageProperty(
            s3_bucket=self._skillasset.s3_bucket_name,
            s3_key=self._skillasset.s3_object_key,
            overrides=alexa_ask.CfnSkill.OverridesProperty(
                manifest={'apis': {'custom': {'endpoint': {'uri': self._function.function_arn}, }, }, }
            ),
            s3_bucket_role=self._skillassetrole.role_arn
        )

        self._skill = alexa_ask.CfnSkill(
            scope=self,
            id='Skill',
            authentication_configuration=self._skillauth,
            skill_package=self._skillpackage,
            vendor_id=self.node.try_get_context('amazon-developer-smapi:vendor-id'),
        )

        # get access to the Level 1 Cfn resource
        self._cfn_function: aws_lambda.CfnFunction = self._function.node.default_child  # type: ignore [no-redef]
        self._skill.add_dependency(self._cfn_function)  # type: ignore [no-redef]

        # allow the Alexa service to invoke the fulfillment Lambda
        # TODO Inside lambda is needed to adjust permissions to new skill ID afterwards
        self._function.add_permission(
            "1",
            principal=aws_iam.ServicePrincipal("alexa-appkit.amazon.com"),
            action="lambda:InvokeFunction",
            # event_source_token=self._skill.ref
        )