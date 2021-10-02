import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="otterpy",
    version="1.0",
    author="Volodymyr Biloshytskyi",
    author_email="volbil@protonmail.com",
    description="Otter - framework for microservices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/volbil/otter",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=[
        "aio-pika==6.8.0",
        "aiormq==3.3.1",
        "async-generator==1.10",
        "deprecation==2.1.0",
        "idna==3.2",
        "kiwipy==0.7.4",
        "marshmallow==3.13.0",
        "multidict==5.1.0",
        "packaging==21.0",
        "pamqp==2.3.0",
        "pyparsing==2.4.7",
        "pytray==0.3.2",
        "PyYAML==5.4.1",
        "shortuuid==1.0.1",
        "yarl==1.6.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
