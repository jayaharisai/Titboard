from setuptools import setup, find_packages

setup(
    name="titboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "typer[all]",
        "boto3"
    ],
    entry_points={
        "console_scripts": [
            "titboard=titboard.cli:main"
        ]
    },
)
