#!/usr/bin/env python3

from aws_cdk import core

from aws_bootstrap_multiaccount.init_stack import InitStack

app = core.App()
InitStack(app, "aws-bootstrap-multiaccount")

app.synth()