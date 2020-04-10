import setuptools

with open("README.md") as fp:
      long_description = fp.read()

setuptools.setup(
      name="aws-bootstrap-multiaccount",
      version="0.0.1",

      description="Python AWS CDK for Setup Initial Payer Account for MultiAccount Environment",
      long_description=long_description,
      long_description_content_type="text/markdown",

      author="bitbauer@outlook.com",

      package_dir={"": "src/cdk_stack"},
      packages=setuptools.find_packages(where="src/cdk_stack"),

      install_requires=[
            "aws-cdk.core",
            "aws-cdk.aws_iam",
            "aws-cdk.aws_lambda",
            "poetry>=1.0.0b1",
      ],

      python_requires=">=3.6",

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
