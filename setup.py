# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fh:
    license = fh.read()

setup(
    name="PiAutoPilot",
    version="0.0.1",
    author="KK Santhanam",
    author_email="KK.Santhanam@gmail.com",
    description="Autopilot for RaspberryPi connected to F7 Flight Controller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    requires=['wheel'],
    url="https://github.com/ksanthanam/PiAutoPilot",
    packages=find_packages(),
    setup_requires=['setuptools','wheel'],
    download_url='https://github.com/KSanthanam/PiAutoPilot/archive/v_01.tar.gz',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license=license,
    python_requires='>=3.6',
    keywords=['RaspberryPi', 'Autopilot', 'F7', 'Betaflight']
)