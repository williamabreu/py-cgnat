# Usage: 
#
# -- Build the project for distribution:
#   python3 setup.py sdist bdist_wheel
# 
# -- Run unit tests:
#   python3 setup.py test


from pycgnat import __version__
import setuptools


setuptools.setup(
    name='pycgnat',
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
    packages=setuptools.find_packages('.', exclude=('pycgnat.tests',)),
    python_requires='>=3.7',
    test_suite='pycgnat.tests',
    keywords='netmap cgnat rfc6598 routeros',
    entry_points={
        'console_scripts': [
            'pycgnat=pycgnat.__main__:main'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking :: Firewalls',
        'Topic :: Utilities',
    ],
)
