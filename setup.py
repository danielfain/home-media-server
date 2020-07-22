import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hms-danielfain", # Replace with your own username
    version="0.0.1",
    author="Daniel Fain",
    author_email="daniel@fain.dev",
    description="Generates a docker-compose file for an automated home media server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielfain/home-media-server",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "PyInquirer",
        "pyyaml"
    ]
)