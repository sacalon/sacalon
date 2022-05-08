from setuptools import setup, find_packages
from hascal import __version__

setup(
    name="hascal",
    version="v1.3.9-alpha.1",
    author="Hascal Foundation",
    description="Hascal is a general purpose and open source programming language designed to build optimal, maintainable, reliable and efficient software.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "requests",
    ],
    entry_points={
        "console_scripts": ["hascal=hascal.hascal:main"],
    },
    package_data={"": ["hascal/hlib/*/**", "hascal/hlib/**"]},
    include_package_data=True,
    python_requires=">=3.7",
)
