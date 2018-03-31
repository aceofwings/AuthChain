from setuptools import setup, find_packages
install_requires = [
    'pysha3~=1.0.2',
    'cryptoconditions~=0.6.0.dev',
    'flask>=0.10.1',
    'flask-cors~=3.0.0',
    'flask-restful~=0.3.0',
    'requests~=2.9',
    'jsonschema~=2.5.1',
    "protobuf>=3.2.0",
    "gevent>=1.2.1",
    "colorlog>=3.0.1",
]

setup(
    name='AuthChain',
    version="0.1.0",
    description= 'AuthChain: BlockChain Authentication',
    long_description=(
        "Using BlockChain an authentication system is built"
        "decentralized from current popular schemes schemes"
        ),
    url='https://github.com/aceofwings/AuthChain',
    author='Daniel Harrington',
    author_email='dxh7006@rit.edu',
    license='Apache Software License 2.0',
    zip_safe=False,
    packages=find_packages(exclude=['tests*']),
    entry_points={
        'console_scripts': [
            'AuthChain=authchain.commands.exec:main'
        ],
    },
    install_requires=install_requires,
    )
