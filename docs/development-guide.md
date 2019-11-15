## Development Guide

### Running the code

`$ python3 -m shallow_backup`

### Testing

```shell
$ pipenv shell
$ pipenv install
$ pytest

####
# Code Coverage
# NOTE: This makes some tests fail -- not sure why. Just ignore those for now.
####

$ py.test --cov --cov-report html:code_coverage 
$ open code_coverage/index.html
```

Make sure all existing tests pass before opening a PR!
Also, add any necessary tests for new code.


### Deployment

- Bump version in `shallow-backup/constants.py`
- Tag commit with `v{VERSION}`: `$ git tag -a v{VERSION} -m "shallow-backup v{VERSION}"`
- Push commit to GitHub.
- Run `$ github_changelog_generator --user alichtman --project shallow-backup`.
- Make another commit with the changelog
- Build the package: `$ pypibinary`
- Create new release: `$ hub release create v{VERSION} --file dist/shallow-backup-{VERSION}.tar.gz -m "shallow-backup v{VERSION}"`
- Push to PyPI with `$ pypiup`

### Code Style

You should follow the code style already established in the code base.

PEP8 is generally to be followed, but I think that prettier code to look at in an editor is more important that strictly following PEP8. 

All files should end with a new line.

PRs with changes in indentation style _will not be merged._ Tabs (width of 4 spaces) should be used.

### Continuous Integration Testing and Static Analysis

+ [Travis CI](https://travis-ci.com/alichtman/shallow-backup)
+ [Codacy](https://app.codacy.com/project/alichtman/shallow-backup/dashboard)
+ [CodeClimate](https://codeclimate.com/github/alichtman/shallow-backup)
+ [Coveralls](https://coveralls.io/github/alichtman/shallow-backup)

