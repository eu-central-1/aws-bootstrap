#!/usr/bin/env python3

import os

# For consistency with other languages, `cdk` is the preferred import name
from aws_cdk import core as cdk

from alexa_cloudstacks.cdk_stack import AlexaCloudstacksStack

# For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
env = cdk.Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION')
)

tags = {
    'CostCenter': 'eu-central-1',
    'Contact': 'max@mustermann.de',
}

app = cdk.App()
for key in tags:
    cdk.Tag.add(app, key, tags[key])

AlexaCloudstacksStack(app, 'Alexa-Cloudstack', env=env)

app.synth()