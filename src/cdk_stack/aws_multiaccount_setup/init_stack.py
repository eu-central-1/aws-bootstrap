from aws_cdk import (
    core
)

from .init_alexacloud_skill import AlexaConstruct

class InitStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        alexa = AlexaConstruct(self, "MyAlexaConstruct")