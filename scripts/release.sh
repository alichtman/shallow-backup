#!/bin/bash
# Release script for shallow-backup

# NOTE: Must be run from project root directory

set -e

# Check if on master
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "master" ]]; then
  echo 'Must be on master branch to cut a release!';
  exit 1;
fi

# Check if master is dirty
if [[ -n $(git status -s) ]]; then
    echo 'Master branch dirty! Aborting.';
    exit 1;
fi

SB_VERSION="v$(python3 -c "from shallow_backup.constants import ProjInfo; print(ProjInfo.VERSION)")"
SB_VERSION_NO_V="$(python3 -c "from shallow_backup.constants import ProjInfo; print(ProjInfo.VERSION)")"

read -r -p "Release shallow-backup $SB_VERSION? Version bump should already be committed and pushed. [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY])
        echo "Releasing."
        ;;
    *)
        echo "Aborting."
        exit;
        ;;
esac

git checkout master && git pull
git tag -a "$SB_VERSION" -m "shallow-backup $SB_VERSION" && git push
github_changelog_generator --user alichtman --project shallow-backup
git add CHANGELOG.md && git commit -m "Add CHANGELOG for $SB_VERSION" && git push
echo "Generating distribution files..."
rm -rf dist/* && python3 setup.py sdist
echo "Creating GH release..."
hub release create "$SB_VERSION" --file "dist/shallow-backup-$SB_VERSION_NO_V.tar.gz" -m "shallow-backup $SB_VERSION"
echo "Uploading to pypi..."
twine upload --repository pypi dist/*
