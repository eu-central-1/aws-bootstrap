Python AWS CDK solution for voice reports about your AWS account
=========

This is a Python project, for Alexa skill that you can use to get reports of your AWS account environment.

## How it Works

This project uses a simple structure for sources, tooling and testing.
Just execute `make` to see what you can do.

**Current status:** Under development

## How to start

You will need to have Python 3.9 installed. After this you just need to call
 ```
 $ make install
 ```

The initialization process also creates a virtualenv within this project, stored under the venv directory.
It will also install AWS cdk command by calling `npm install -g aws-cdk`.

### Python

It is tested with Python 3.8.x.
You can use `source ./install_venv.sh` to create Python environment for this project.
After that you need to run `make install` to add required packages for CDK project. 

To add additional dependencies, for example other CDK libraries, just add
them to your `requirements.txt` file and rerun `make install`

To add additional dependencies, for AWS Lambda, just add them to the `requirements-dev.txt` and into `requirements.txt`file in `lambda` subfolder.After that you need to rerun `source ./install_venv.sh` command.

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
[Install ASK cli](https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html) and run
```
ask configure
```

Then read carefully https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ask-skill-authenticationconfiguration.html 
Finally add your LWA credentials to `~/.cdk.json` file.

Now please deploy a new Alexa Skill Model.
```
ask new
```
Answer the questions for setup process as following:
```
? Choose the programming language you will use to code your skill
- Python
```
```
? Choose a method to host your skill's backend code
- Self-Hosted
```
```
? Choose a template to start with
- Hello world		  Alexa's hello world skill to send the greetings to the world!
```
```
? Please type in your skill name:
- aws-command
```
```
? Please type in your folder name for the skill project (alphanumeric):
- ask_playground
```

### AWS CDK

If you use profiles for AWS CLI, you will need to set `--profile` parameter in every command.

For reference on AWS CDK visit: https://docs.aws.amazon.com/de_de/cdk

If you never used cdk with the target AWS account and region, you need to bootstrap it.
```
$ cdk bootstrap
```

At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

Finally, use deploy command to deploy template as CloudFormation stack.
```
cdk deploy --parameters skill=amzn1.ask.skill.12345678-2222-3333-4444-123456789abc
```

| Parameter | Description |
|-----------|-------------|
| skill     | ID of Alexa skill created in AWS developer account |

The `cdk.json` file tells the CDK Toolkit how to execute your app.

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

* **Python** for CDK code and AWS Lambda implementation
* **NodeJS** and npm for cli commands for CDK and ASK
* **Docker** to build AWS Lambda archive locally with CDK

## License

This project is licensed under the terms of the MIT license.