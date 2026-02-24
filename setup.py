#!/usr/bin/env python3
"""Setup configuration for CodeWise."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="codewise",
    version="2.0.0",
    author="Abhishek Kumar",
    author_email="abhishekkumar@iiitdmj.ac.in",
    description="Multi-language AI-powered code review system for automated PR analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abhishek27iiitdmj/codewise",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "codewise=ai_reviewer:main",
        ],
    },
)
