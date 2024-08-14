from setuptools import setup, find_packages

setup(
    name="jupiterone-cli",
    version="0.1.0",
    description="A CLI client for JupiterOne API",
    author="James Mountifield",
    author_email="james.mountifield@gmail.com",
    packages=find_packages(),
    install_requires=[
        "jupiterone==1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "jupiterone-cli=jupiterone_cli.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
