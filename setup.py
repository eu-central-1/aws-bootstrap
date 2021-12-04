import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="aws-bootstrap",
    version="0.1.0-alpha.0",

    description="Python AWS CDK for bootstrapping initial payer account for multi-account environment",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="4582513+bitbauer@users.noreply.github.com",

    package_dir={"": "src/cdk_stack"},
    packages=setuptools.find_packages(where="src/cdk_stack"),

    install_requires=[
        "aws-cdk.core==1.77.0",
        "aws-cdk.aws_iam==1.77.0",
        "aws-cdk.aws_lambda==1.77.0"
    ],

    python_requires=">=3.8",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
