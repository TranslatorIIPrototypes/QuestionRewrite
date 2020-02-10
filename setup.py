"""Setup file for QRW package."""
from setuptools import setup

setup(
    name='Question ReWrite',
    version='1.0.0',
    author='Phil Owen',
    author_email='powen@renci.org',
    url='https://github.com/patrickkwang/r3',
    description='Question rewrite - Offers additional relevant questions based initial question asked.',
    packages=['QRW'],
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    python_requires='>=3.7',
)
