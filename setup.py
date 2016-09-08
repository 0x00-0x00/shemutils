from setuptools import setup

setup(name='shemutils',
      version='0.1.4',
      description='Shemhazai Utilities',
      url='https://bitbucket.org/itslikeme/shemutils',
      author='Shemhazai',
      author_email='nestorm2486@gmail.com',
      license='MIT',
      packages=['shemutils'],
      package_dir={"shemutils": "src"},
      package_data={"shemutils": ["src/*"]},
      zip_safe=False)
