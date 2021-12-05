from aws_cdk import (
    core
)

from .init_cloudstacks_skill import AlexaConstruct


class InitStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        skill_id = core.CfnParameter(
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


