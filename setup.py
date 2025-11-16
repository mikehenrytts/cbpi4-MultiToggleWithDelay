from setuptools import setup

setup(name='cbpi4-plugin-MultiToggleWithDelay',
      version='1.0.0',
      description='CraftBeerPi Plugin',
      author='Mike Henry',
      author_email='',
      url='',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4-plugin-MultiToggleWithDelay': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4-plugin-MultiToggleWithDelay'],
     )
