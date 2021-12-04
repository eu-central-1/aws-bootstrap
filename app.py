#!/usr/bin/env python3

import os

from aws_cdk import core

from aws_bootstrap.init_stack import InitStack


# For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
env = core.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION')
)

app = core.App()
InitStack(app, "aws-bootstrap", env=env)
app.synth()