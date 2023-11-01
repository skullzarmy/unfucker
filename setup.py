from setuptools import setup, find_packages

setup(
    name='Unfucker',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'unfucker=unfucker.unfucker:unfuck_entry',
        ],
    }
)
