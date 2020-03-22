#!/bin/bash
# Release script for shallow-backup

# Must be run from project root directory
SB_VERSION="v$(python3 -c "from shallow_backup.constants import ProjInfo; print(ProjInfo.VERSION)")"
SB_VERSION_NO_V="$(python3 -c "from shallow_backup.constants import ProjInfo; print(ProjInfo.VERSION)")"

read -r -p "Release shallow-backup $SB_VERSION? [y/N] " response
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
ga . && gc -m "Add CHANGELOG for $SB_VERSION" && git push
rm -rf dist/* && python3 setup.py sdist
hub release create $SB_VERSION --file dist/shallow-backup-$SB_VERSION_NO_V.tar.gz -m "shallow-backup $SB_VERSION"
pypiup
