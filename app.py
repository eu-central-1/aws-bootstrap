#!/usr/bin/env python3

from aws_cdk import core

from cdk_stack.aws_multiaccount_setup.init_stack import InitStack

app = core.App()
InitStack(app, "aws-bootstrap-multiaccount")

app.synth()