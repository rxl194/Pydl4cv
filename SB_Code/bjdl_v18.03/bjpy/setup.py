
from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [ 'opencv-python' ]

setup(
    name='bjdl_c07_knn',
    version='0.0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='BJDL Ch07 KNN'
)

