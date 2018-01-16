from setuptools import setup, find_packages

setup(
    name='mbta',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/milas/python-mbta',
    license='MIT',
    author='Milas Bowman',
    author_email='milasb@gmail.com',
    description='Python library for MBTA v3 realtime API',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'iso8601',
        'jsonapi-requests',
        'requests'
    ]
)
