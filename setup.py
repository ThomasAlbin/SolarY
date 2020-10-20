import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="solary",
    version="0.1",
    author="Thomas Albin",
    packages=setuptools.find_packages(),
    package_data={'solary': ['_config/constants.ini']},
    include_package_data=True,
    description="TBD",
    long_description=long_description,
    url="https://github.com/ThomasAlbin/SolarY",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
)
