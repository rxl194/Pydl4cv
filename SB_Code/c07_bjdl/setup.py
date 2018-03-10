from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [ 'opencv-python>=3.2' ]

setup(
    name='cvdl_c07_knn',
    version='0.0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='CVDL Ch07 KNN'
)

