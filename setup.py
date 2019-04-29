from setuptools import setup, find_packages


setup(
    name='basic_aio_api',
    version=0.1,
    packages=find_packages('.'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'aio_api_start = server:start_server'
        ],
    },
    install_requires=[
        'aiohttp',
        'cerberus',
    ],
)
