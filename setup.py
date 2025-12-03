import re
from pathlib import Path

import pkg_resources as pkg
import setuptools

FILE = Path(__file__).resolve()
PARENT = FILE.parent  # root directory
README = (PARENT / "README.md").read_text(encoding="utf-8")
REQUIREMENTS = [
    f"{x.name}{x.specifier}"
    for x in pkg.parse_requirements((PARENT / "requirements.txt").read_text())
]


def get_version():
    file = PARENT / "pivotcrop/__init__.py"
    return re.search(
        r'^__version__ = [\'"]([^\'"]*)[\'"]',
        file.read_text(encoding="utf-8"),
        re.M,
    )[1]


setuptools.setup(
    name="pivotcrop",
    version="0.1.1",
    author="Josiah Putman",
    description="Package for cropping directories of images based on a pivot.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={"Source": "https://github.com/Katsutoshii/pivotcrop"},
    python_requires=">=3.13",
    install_requires=REQUIREMENTS,
    url="https://github.com/Katsutoshii/pivotcrop",
    extras_require={
        "dev": [
            "check-manifest",
            "pytest",
            "pytest-cov",
            "coverage",
            "mkdocs",
            "mkdocstrings[python]",
            "mkdocs-material",
        ]
    },
)
