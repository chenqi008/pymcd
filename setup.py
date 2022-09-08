from setuptools import setup, find_packages
import pymcd

from pathlib import Path
this_directory = Path(__file__).parent

VERSION = '0.2.0' 
DESCRIPTION = 'Calculate Mel-Cepstral Distortion (MCD)'
LONG_DESCRIPTION = (this_directory/"README.md").read_text()

setup(
    name="pymcd", 
    version=VERSION,
    author="QiChen",
    author_email="<chenqi.china@outlook.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    license="MIT",
    readme = "README.md",
    url = "https://github.com/chenqi008/pymcd",
    packages=find_packages(),
    install_requires=[
        "librosa",
        "numpy",
        "pyworld",
        "pysptk",
        "fastdtw",
        "scipy",
        ],
    keywords=['python', 'Mel-Cepstral Distortion (MCD)'],
    classifiers= [
        "Programming Language :: Python :: 3",
    ]
)