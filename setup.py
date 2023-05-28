import re

from setuptools import setup

with open("explain/__init__.py") as f:
    version = re.search(r"\d.\d.\d", f.read()).group(0)  # type: ignore

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="explain",
    version=version,
    py_modules=["explain"],
    # packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "explain = explain:cli",
        ],
    },
)
