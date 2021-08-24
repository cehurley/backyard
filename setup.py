#!/usr/bin/env python
from setuptools import setup, find_packages

version = "0.0.1"

with open("./README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="backyard",
    version=version,
    url="https://github.com/cehurley/backyard",
    project_urls={
        "Documentation": "https://github.com/cehurley/backyard",
    },
    description="Simple Python MySQL/MariaDB ORM",
    long_description=readme,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'pymysql',
        'python-dotenv',
        'psutil'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Database",
    ],
    keywords="ORM",
)
