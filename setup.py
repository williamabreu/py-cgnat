import setuptools
import toml

import pycgnat as src

config = toml.load("pyproject.toml")["tool"]["poetry"]
config["author"] = ", ".join(
    [" ".join(name_email.split()[:-1]) for name_email in config["authors"]]
)
config["author_email"] = ", ".join(
    [name_email.split()[-1][1:-1] for name_email in config["authors"]]
)

setuptools.setup(
    name=config["name"],
    version=config["version"],
    license=config["license"],
    author=config["author"],
    author_email=config["author_email"],
    description=config["description"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/williamabreu/py-cgnat",
    install_requires=open("requirements.txt").read().splitlines(),
    platforms="any",
    packages=setuptools.find_packages(".", exclude=("tests", "tests.*")),
    python_requires=">=3.7",
    test_suite="tests",
    keywords="netmap cgnat rfc6598 routeros",
    entry_points={
        "console_scripts": [f"pycgnat={src.__name__}.__main__:main"]
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: Utilities",
    ],
)
