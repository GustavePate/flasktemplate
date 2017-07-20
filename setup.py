from setuptools import setup

setup(
    name='flasktemplate',
    version='0.1.0',
    author='G. Pate',
    author_email='gpate@yopmail.com',
    packages=['flasktemplate', 'flasktemplate.tests'],
    scripts=['bin/launcher.sh'],
    url='http://pypi.python.org/pypi/flasktemplate/',
    license='LICENSE.txt',
    description='a template',
    long_description=open('README.rst').read(),
    include_package_data=True,
    install_requires=[
        'flask',
        'colorlog',
        'flask-swagger-ui',
        'flask-restful-swagger-2',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
