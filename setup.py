from setuptools import setup
from codecs import open
from os import path
from constants import Constants

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name=Constants.PROJECT_NAME,  # Required
    version=Constants.VERSION,  # Required
    description=Constants.DESCRIPTION,  # Required
    long_description_content_type="text/markdown",
    long_description=long_description,
    url=Constants.URL,
    author=Constants.AUTHOR_GITHUB,
    # author_email=Constants.AUTHOR_EMAIL,
    author_email="aaronlichtman@gmail.com",

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        'Development Status :: 4 - Beta',

        'Environment :: MacOS X',

        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',

        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Operating System',
        'Topic :: Documentation',
        'Topic :: Utilities',

        'Operating System :: MacOS',

        'Natural Language :: English',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='backup documentation system dotfiles install list configuration',  # Optional

    # Just want to distribute a single Python file, so using `py_modules`
    # argument as follows, which will expect a file called
    # `stronghold.py` to exist:
    #
    py_modules=[
        "shallow_backup",
        "constants"
    ],

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'inquirer>=2.2.0',
        'colorama>=0.3.9',
        'Click'
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={
        'console_scripts':'shallow-backup=shallow_backup:cli'
    },

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
        'Bug Reports': 'https://github.com/alichtman/shallow-backup/issues',
        'Donations': 'https://www.patreon.com/alichtman',
    },
)
