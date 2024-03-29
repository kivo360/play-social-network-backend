from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="yaggal",
    version="0.0.1",
    author="Kevin Hill",
    author_email="kevin@funguana.com",
    description="Yours.org ripoff site",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["yaggal"],
    install_requires=['sanic', 'funtime', 'dask[dataframe]'],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
    
)
