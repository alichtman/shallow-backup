#!/bin/bash
# Release script for shallow-backup

set -e

# Check if .git directory exists
if [[ ! -d ".git" ]]; then
  echo 'Must be run from project root directory!';
  exit 1;
fi

# Check if on main
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "main" ]]; then
  echo 'Must be on main branch to cut a release!';
  exit 1;
fi

# Check if main is dirty
if [[ -n $(git status -s) ]]; then
    echo 'main branch dirty! Aborting.';
    exit 1;
fi

SB_VERSION_NO_V="$(python3 -c "from shallow_backup.constants import ProjInfo; print(ProjInfo.VERSION)")"
SB_VERSION="v$SB_VERSION_NO_V"

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

git checkout main && git pull
git tag -a "$SB_VERSION" -m "shallow-backup $SB_VERSION" && git push
github_changelog_generator --user alichtman --project shallow-backup
git add CHANGELOG.md && git commit -m "Add CHANGELOG for $SB_VERSION" && git push
echo "Generating distribution files..."
rm -rf dist/* && python3 setup.py sdist
echo "Creating GH release..."
set +x
echo "$SB_VERSION"
gh release create "shallow-backup $SB_VERSION" "dist/shallow-backup-$SB_VERSION_NO_V.tar.gz" --notes "shallow-backup $SB_VERSION"
set -x
echo "Uploading to pypi..."
twine upload --repository pypi dist/*
