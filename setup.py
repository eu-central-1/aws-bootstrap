import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="aws-demo",
    version="0.3.0-alpha.0",

    description="Python AWS CDK solution for voice reports about your AWS account",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="4582513+bitbauer@users.noreply.github.com",

    python_requires=">=3.8",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
