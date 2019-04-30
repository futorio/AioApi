from setuptools import setup, find_packages


setup(
    name='basic_aio_api',
    version=0.1,
    packages=find_packages('.'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'telegram_stat_api = aioapi:main'
        ],
    },
    install_requires=[
        'aiohttp',
        'cerberus',
    ],
)
