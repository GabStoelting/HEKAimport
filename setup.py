from setuptools import find_packages, setup
setup(
    name='HEKAimport',
    packages=find_packages(include=["HEKAimport"]),
    version='0.1.0',
    description='Library to import HEKA Patchmaster files',
    author='Gabriel Stoelting',
    license='GPL-3.0',
)