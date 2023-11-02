from setuptools import setup, find_packages

setup(
    name='Unfucker',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'attrs==23.1.0',
        'chardet==5.2.0',
        'exceptiongroup==1.1.3',
        'iniconfig==2.0.0',
        'packaging==23.2',
        'pluggy==1.3.0',
        'pytest==7.4.2',
        'tomli==2.0.1',
        'python-magic==0.4.27',
    ],
    extras_require={
        'bin': ['python-magic-bin==0.4.14'],
    },
    entry_points={
        'console_scripts': [
            'unfucker=unfucker.unfucker:unfuck_entry',
        ],
    }
)
