Python AWS CDK for setup Payer Account with MultiAccount Environments
=========

This is a Python project, for bootstrapping initial Payer Account for MultiAccount Environments.

## How it Works

This project uses a simple structure for sources, tooling and testing.
Just execute `make` to see what you can do.

**Current status:** First release

## How to start

You will need to have Python 3 installed. After this you just need to call
 ```
 $ make install
 ```

The initialization process also creates a virtualenv within this project, stored under the venv directory.
It will also install AWS cdk command by calling `npm install -g aws-cdk`.

### Python

It is tested with Python 3.7.x.
You can use `make venv` to create Python environment for this project.

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

### PyTest

This project uses PyTest for a simple testing approach.
For reference visit: https://docs.pytest.org/en/latest/index.html

### AWS CDK

At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

The `cdk.json` file tells the CDK Toolkit how to execute your app.
For reference on AWS CDK visit: https://docs.aws.amazon.com/de_de/cdk

### Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

## Prerequisites

### Local development

This is developed to support development under Mac OS X, Windows and Linux (Ubuntu, CentOS).
For local testing you will need to install Python 3.7.x.

## Dependencies

None (... because it is already managed by GNU make)

## License

This project is licensed under the terms of the MIT license.