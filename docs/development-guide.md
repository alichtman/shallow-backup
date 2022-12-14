## Development Guide

### Running the code

```bash
$ pipenv shell
$ pipenv install --dev
$ python3 -m shallow_backup
```

### Testing

```bash
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

Make a version bump commit, like:

```diff
From d71b903dacd5eeea9d0be68ef3022817f9bac601 Mon Sep 17 00:00:00 2001
From: Aaron Lichtman <aaronlichtman@gmail.com>
Date: Sun, 19 Jun 2022 05:46:06 -0500
Subject: [PATCH] Version bump to v5.2

---
 shallow_backup/constants.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

diff --git a/shallow_backup/constants.py b/shallow_backup/constants.py
index 7edcb5c3..13b949c4 100644
--- a/shallow_backup/constants.py
+++ b/shallow_backup/constants.py
@@ -1,6 +1,6 @@
 class ProjInfo:
 	PROJECT_NAME = 'shallow-backup'
-	VERSION = '5.1'
+	VERSION = '5.2'
 	AUTHOR_GITHUB = 'alichtman'
 	AUTHOR_FULL_NAME = 'Aaron Lichtman'
 	DESCRIPTION = "Easily create lightweight backups of installed packages, dotfiles, and more."
```

And then run `scripts/release.sh` from the project root.

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
