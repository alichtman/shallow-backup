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

```bash
$ export SB_RELEASE_VERSION="v{VERSION}VERSION"
$ git checkout master && git pull
$ git tag -a $SB_RELEASE_VERSION -m "shallow-backup $SB_RELEASE_VERSION" && git push
$ github_changelog_generator --user alichtman --project shallow-backup
$ ga . && gc -m "Add CHANGELOG for $SB_RELEASE_VERSION" && git push
$ pypibinary
$ hub release create $SB_RELEASE_VERSION --file dist/shallow-backup-$SB_RELEASE_VERSION.tar.gz -m "shallow-backup $SB_RELEASE_VERSION"
$ pypiup
```

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

