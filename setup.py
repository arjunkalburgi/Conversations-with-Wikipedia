from distutils.core import setup

setup(
    name='uncover_discover',
    author='Arjun Kalburgi',
    author_email='askalburgi@gmail.com',
    url='https://github.com/askalburgi/uncover_discovery',
    description='CLI learning application',
    long_description=open('README.md').read(),

    version='0.1dev',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    
    packages=['uncover_discover', ],
    install_requires=[
        'wikipedia',
        'watson_developer_cloud'
    ],
)
