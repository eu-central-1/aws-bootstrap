#!/usr/bin/env python3

# For consistency with other languages, `cdk` is the preferred import name
from aws_cdk import core as cdk

from alexa_cloudstacks.cdk_stack import AlexaCloudstacksStack


tags = {
    'CostCenter': 'eu-central-1',
    'Contact': 'max@mustermann.de',
}

app = cdk.App()
for key in tags:
    cdk.Tag.add(app, key, tags[key])

AlexaCloudstacksStack(app, 'Alexa-Cloudstack')

app.synth()