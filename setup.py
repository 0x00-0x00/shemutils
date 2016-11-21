from distutils.core import setup

setup(
    name='shemutils',
    version='0.2',
    packages=['shemutils'],
    package_dir={"shemutils": "src"},
    package_data={"shemutils": ["src/*"]},
    url='http://github.com/0x00-0x00/shemutils',
    license='MIT',
    author='shemhazai',
    author_email='andre.marques@fatec.sp.gov.br',
    description='More information on github README.md'
)
