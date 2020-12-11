#!/usr/bin/env python3

from aws_cdk import core

from aws_bootstrap.init_stack import InitStack

app = core.App()
InitStack(app, "aws-bootstrap")
app.synth()