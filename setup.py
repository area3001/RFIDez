import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yhy522",
    version="0.0.1",
    author="Bert Outtier",
    author_email="outtierbert@gmail.com",
    description="Python library for the yhy522 RFID reader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/area3001/RFIDez",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv2 License",
        "Operating System :: OS Independent",
    ),
    install_requires=['pyserial'],
)

