from setuptools import setup, find_packages

setup(
    name='logtool',
    version='0.1.0',
    description='A distributed log processing CLI tool with export and visualization',
    author='c0mmand3r',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'faker',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'logtool=logtool.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
