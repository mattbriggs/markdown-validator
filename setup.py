from setuptools import setup

setup(
    name='markdownvalidator',
    version='0.1.0',    
    description='A markdownparser and validator.',
    url='https://github.com/mattbriggs/markdown-validator',
    author='Matt Briggs',
    author_email='matt_d_briggs@hotmail.com',
    license='MIT',
    packages=['markdownvalidator'],
    install_requires=['atomicwrites==1.4.0',
                        'attrs==21.4.0',
                        'click==8.1.3',
                        'colorama==0.4.4',
                        'html2text==2020.1.16',
                        'importlib-metadata==4.11.4',
                        'iniconfig==1.1.1',
                        'joblib==1.1.0',
                        'lxml==4.9.0',
                        'Markdown==3.3.7',
                        'nltk==3.7',
                        'packaging==21.3',
                        'pluggy==1.0.0',
                        'py==1.11.0',
                        'pyparsing==3.0.9',
                        'pytest==7.1.2',
                        'PyYAML==6.0',
                        'regex==2022.6.2',
                        'tomli==2.0.1',
                        'tqdm==4.64.0',
                        'zipp==3.8.0',
                      ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.9',
    ],
)