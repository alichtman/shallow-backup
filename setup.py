from os import path
from codecs import open
from setuptools import setup
from shallow_backup.constants import ProjInfo

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=ProjInfo.PROJECT_NAME,
    version=ProjInfo.VERSION,
    description=ProjInfo.DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url=ProjInfo.URL,
    author=ProjInfo.AUTHOR_GITHUB,
    author_email="aaronlichtman@gmail.com",
    # Classifiers help users find your project by categorizing it.
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Operating System",
        "Topic :: Documentation",
        "Topic :: Utilities",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords="backup documentation system dotfiles install list configuration",  # Optional
    packages=["shallow_backup"],
    install_requires=[
        "inquirer>=2.2.0",
        "colorama>=0.3.9",
        "gitpython>=3.1.20",
        "Click",
    ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={"console_scripts": "shallow-backup=shallow_backup.__main__:cli"},
    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={
        "Bug Reports": ProjInfo.BUG_REPORT_URL,
        "Donations": "https://www.patreon.com/alichtman",
    },
)
