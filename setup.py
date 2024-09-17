from setuptools import setup, find_packages

setup(
    name='markdownvalidator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['atomicwrites==1.4.0',
                        'attrs==21.4.0',
                        'click==8.1.3',
                        'colorama==0.4.4',
                        'html2text==2024.2.26',
                        'importlib-metadata==4.11.4',
                        'iniconfig==1.1.1',
                        'joblib==1.2.0',
                        'lxml==5.3.0',
                        'Markdown==3.3.7',
                        'nltk==3.7',
                        'packaging==21.3',
                        'pluggy==1.5.0',
                        'py==1.11.0',
                        'pyparsing==3.0.9',
                        'pytest==8.3.3',
                        'PyYAML==6.0.2',
                        'regex==2022.6.2',
                        'tomli==2.0.1',
                        'tqdm==4.64.0',
                        'zipp==3.8.0',
                      ],
    python_requires='>=3.12',
    include_package_data=True,
    description="A markdownparser and validator.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mattbriggs/markdown-validator',
    author='Matt Briggs',
    author_email='matt_d_briggs@hotmail.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)