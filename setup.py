import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="aws-bootstrap",
    version="0.0.1",

    description="Python AWS CDK for bootstrapping initial payer account for multi-account environment",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="4582513+bitbauer@users.noreply.github.com",

    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),

    install_requires=[
        f"{x}==1.127.0" for x in
        [
            'aws-cdk.core',
            'aws-cdk.aws-iam',
            'aws-cdk.aws-lambda',
            'aws-cdk.aws-lambda-python',
        ]
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
