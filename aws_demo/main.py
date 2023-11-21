from aws_cdk import Stack, CfnParameter
from constructs import Construct
from .alexa_aws_skill.construct import AlexaConstruct


class AlexaDemoStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        skill_id = CfnParameter(
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
