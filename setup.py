"""  Created on 15/04/2024::
------------- setup.py -------------
 
**Authors**: L. Mingarelli
"""
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

about = {}
with open("ecbdata/__about__.py") as f:
    exec(f.read(), about)


with open("requirements.txt") as f:
    install_requirements = f.read().splitlines()

setuptools.setup(
    name="ecbdata",
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__email__'],
    description=about['__about__'],
    url=about['__url__'],
    license='MIT',
    long_description=long_description,
    long_description_content_type="markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


