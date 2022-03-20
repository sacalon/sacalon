import setuptools
from hascal import version

setuptools.setup(
    name="hascal",
    version=version,
    author="Hascal Foundation",
    description="Hascal is a general purpose and open source programming language designed to build optimal, maintainable, reliable and efficient software.",
    packages=setuptools.find_packages(),
    install_requires=[
        "colorama",
        "requests",
    ],
    entry_points={
        "console_scripts": ["hascal=hascal.hascal:main"],
    },
    package_data={"": ["hascal/hlib/*/**", "hascal/hlib/**"]},
    include_package_data=True,
    python_requires=">=3.5",
)
