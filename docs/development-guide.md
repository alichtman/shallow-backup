## Development Guide

### Running the code

`$ python3 -m shallow_backup`

### Testing

```shell
$ cd tests
$ pipenv run python3 -m pytest
```

Make sure all existing tests pass before opening a PR!
Also, add any necessary tests for new code. I'd like to have a lot more of this code base under CI testing, as opposed to manual testing.

### Code Style

You should follow the code style already established in the code base.

PEP8 is generally to be followed, but I think that prettier code to look at in an editor is more important that strictly following PEP8. 

All files should end with a new line.

PRs with changes in indentation style _will not be merged._ Tabs (width of 4 spaces) should be used.
