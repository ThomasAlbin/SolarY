import setuptools

import solary

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='solary',
    version=solary.__version__,
    author=solary.__author__,
    packages=setuptools.find_packages(),
    package_data={'solary': ['_config/constants.ini', '_config/paths.ini']},
    include_package_data=True,
    description="A Space Science library for asteroid, comets and meteors",
    url="https://github.com/ThomasAlbin/SolarY",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
    install_requires=[
        "pytest>=6.1.0",
        "certifi"
    ],
)
