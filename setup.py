from setuptools import setup

package_name = 'exchanges'

setup(name=package_name,
      version='0.1',
      description=('A Python package that provides a uniform interface to'
                   'crypto currency exchanges'),
      url='https://github.com/black-omen/exchanges',
      author='Black Omen',
      author_email='',
      include_package_data=True,
      packages=[package_name])
