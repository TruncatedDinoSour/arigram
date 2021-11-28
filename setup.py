from setuptools import setup

import arigram

with open("README.md", "r") as fh:
    readme = fh.read()


setup(
    long_description=readme,
    long_description_content_type="text/markdown",
    name="arigram",
    version=arigram.__version__,
    description="A fork of tg -- a hackable telegram TUI client",
    url="https://github.com/TruncatedDinosour/arigram",
    author="TruncatedDinosour",
    author_email="truncateddinosour@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["arigram"],
    entry_points={"console_scripts": ["arigram = arigram.__main__:main"]},
    python_requires=">=3.8",
    install_requires=["python-telegram==0.14.0", "pyfzf==0.2.2"],
)
