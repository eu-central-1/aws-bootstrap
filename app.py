import os
from aws_cdk import App, Environment, Tags
from aws_demo.main import AlexaDemoStack

# for development, use account/region from cdk cli
dev_env = Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION')
)

tags = {
     'CostCenter': 'eu-central-1',
     'Contact': 'max@mustermann.de',
}

app = App()
for key in tags:
    Tags.of(app).add(key, tags[key])

AlexaDemoStack(app, "aws-demo", env=dev_env)

app.synth()
