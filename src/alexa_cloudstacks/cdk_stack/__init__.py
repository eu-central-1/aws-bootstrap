# For consistency with other languages, `cdk` is the preferred import name
from aws_cdk import core as cdk

from .alexa_construct import AlexaConstruct


class AlexaCloudstacksStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        skill_id = cdk.CfnParameter(
            self,
            id="skill",
            type="String",
            description="The id of the Amazon ASK skill, that triggers lambda."
        ).value_as_string

        # The code that defines your stack goes here
        self._alexa = AlexaConstruct(
            self,
            id="alexa",
            skill_id=skill_id
        )


