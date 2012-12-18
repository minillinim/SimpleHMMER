from distutils.core import setup

setup(
    name='SimpleHMMER',
    version='0.2.3',
    author='Michael Imelfort',
    author_email='mike@mikeimelfort.com',
    packages=['simplehmmer', 'simplehmmer.test'],
    scripts=[],
    url='http://pypi.python.org/pypi/SimpleHMMER/',
    license='GPL3',
    description='SimpleHMMER',
    long_description=open('README.txt').read(),
    install_requires=[],
)
