from setuptools import setup

setup(
    name='pyPLCnext',
    version='1.0.1',
    packages=[''],
    url='https://github.com/AlexanderSkachkov/PyPLCnext',
    license='MIT',
    install_requires=['requests==2.24.0'],
    setup_requires=['requests==2.24.0'],
    author='Alexander Skachkov',
    author_email='lex.skachkov.it@gmail.com',
    description='A very simple REST library to use variables in PLCnext AXC F 2152 PLC from Python.'
)
