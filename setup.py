from setuptools import setup, find_packages
import pymcd

VERSION = '0.1.0' 
DESCRIPTION = 'Calculate Mel-Cepstral Distortion (MCD)'
LONG_DESCRIPTION = 'Python package for calculating Mel-Cepstral Distortion (MCD) value between two audios'

setup(
    name="pymcd", 
    version=VERSION,
    author="QiChen",
    author_email="<chenqi.china@outlook.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
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