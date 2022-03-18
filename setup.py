import setuptools
print(setuptools.find_packages())
setuptools.setup(
    name='hascal',
    version='1.3.8-alhpa',
    author='Hascal Foundation',
    description='Hascal is a general purpose and open source programming language designed to build optimal, maintainable, reliable and efficient software.',

    packages=setuptools.find_packages(),
    install_requires=[
        'colorama',
        'requests',
    ],
    entry_points = {
        'console_scripts': ['hascal=hascal.hascal:main'],
    },
    package_data={
        '' : ['hascal/hlib/*/**','hascal/hlib/**']
    },
    include_package_data=True,
    python_requires='>=3.5'
)