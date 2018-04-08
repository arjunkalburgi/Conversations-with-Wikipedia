from distutils.core import setup

setup(
    name='Conversations-with-Wikipedia',
    author='Arjun Kalburgi',
    author_email='askalburgi@gmail.com',
    url='https://github.com/askalburgi/Conversations-with-Wikipedia',
    description='CLI learning application',
    long_description=open('README.md').read(),

    version='0.1dev',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    
    packages=['Conversations-with-Wikipedia', 'Conversations-with-Wikipedia.dependencies'],
    install_requires=[
        'wikipedia',
        'wikipediaapi',
        'inquirer', 
        'random',
        'watson_developer_cloud'
    ],
)
