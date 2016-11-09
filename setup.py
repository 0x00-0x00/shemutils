from distutils.core import setup

setup(
    name='shemutils',
    version='0.1.7',
    packages=['shemutils'],
    package_dir={"shemutils": "src"},
    package_data={"shemutils": ["src/*"]},
    url='http://github.com/0x00-0x00',
    license='MIT',
    author='shemhazai',
    author_email='andre.marques@fatec.sp.gov.br',
    description='ShemUtils package'
)
