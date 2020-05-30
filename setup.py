# Usage: 
#   python3 setup.py sdist bdist_wheel

import setuptools

from py_cgnat import __version__


setuptools.setup(
    name='py-cgnat',
    version=__version__,
    license='MIT License',
    author='William Abreu',
    author_email='contato@williamabreu.net',
    description='Python module for generating CGNAT rules using netmap',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/williamabreu/py-cgnat',
    install_requires=open('requirements.txt').read().splitlines(),
    platforms='any',
    packages=setuptools.find_packages('.', exclude=('tests',)),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'py-cgnat=py_cgnat.__main__:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
