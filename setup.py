from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='truth',
    version='0.1',
    url='https://github.com/jujinkim/truth',
    author='Jujin Kim',
    author_email='jujin@jujinkim.com',
    description='Automated Tistory post translation and HUGO post creation',
    packages=find_packages(),
    install_requires=required,
)