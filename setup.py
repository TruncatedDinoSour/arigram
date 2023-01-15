from setuptools import setup

import arigram

with open("README.md", "r") as fh:
    readme = fh.read()

with open("requirements.txt", "r") as fr:
    reqs = list(map(str.strip, fr.readlines()))

setup(
    long_description=readme,
    long_description_content_type="text/markdown",
    name="arigram",
    version=arigram.__version__,
    description="A fork of tg -- a hackable telegram TUI client",
    url="https://github.com/TruncatedDinosour/arigram",
    author="TruncatedDinosour",
    author_email="ari.web.xyz@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=["arigram"],
    entry_points={"console_scripts": ["arigram = arigram.__main__:main"]},
    python_requires=">=3.10",
    install_requires=reqs,
)
