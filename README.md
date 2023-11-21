Python AWS CDK solution for bootstrapping of multi-account environments
=========

This is a Python project, for bootstrapping initial payer account for AWS multi-account environments.

## How it Works

This project uses a simple structure for sources, tooling and testing.
Just execute `make` to see what you can do.

**Current status:** Under development

## How to start

You will need to have Python 3.8 installed. After this you just need to call
 ```
 $ make install
 ```

The initialization process also creates a virtualenv within this project, stored under the venv directory.
It will also install AWS cdk command by calling `npm install -g aws-cdk`.

### Python

It is tested with Python 3.8.x.
You can use `make .venv` to create Python environment for this project.

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `make install`
command.

### PyTest

Project uses PyTest for a simple testing approach.
For reference visit: https://docs.pytest.org/en/latest/index.html

### AWS CDK

At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

After this, use deploy command to deploy CloudFormation stack with related skill id parameter.
```
cdk deploy --parameters skill=amzn1.ask.skill.your-skill-guid-number
```

The `cdk.json` file tells the CDK Toolkit how to execute your app.
For reference on AWS CDK visit: https://docs.aws.amazon.com/de_de/cdk

This CDK stack requires LWA credentials and further IDs for [Alexa Skill Kit](#amazon-ask). It needs to be stored in `.cdk.json` file in user home directory as following. 
```
{
  "context": {
    "amazon-developer-smapi:vendor-id": "your-vendor-id",
    "amazon-developer-smapi:client-id": "amzn1.application-oa2-client.123",
    "amazon-developer-smapi:client-secret": "abc",
    "amazon-developer-smapi:refresh-token": "ABC"
  }
}
```

CDK doesn't support [AWS SSO profiles](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html) in `~/.aws/config` file. As a workaround you can use [aws-sso-util](https://github.com/benkehoe/aws-sso-util)

### Amazon ASK

It's required to install ASK CLI to deploy an Alexa Skill Model.
Install ASK cli and run
```
ask configure
```
Then read carefully https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-authenticationconfiguration.html 
Finally add your LWA credentials to `~/.cdk.json` file.

### Useful CDK commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

## Prerequisites

### Local development

This is developed to support development under Mac OS X, Windows and Linux (Ubuntu, CentOS).
For local testing you will need to install Python 3.8.x.

## Dependencies

None (... because it is already managed by GNU make)

## License

This project is licensed under the terms of the MIT license.