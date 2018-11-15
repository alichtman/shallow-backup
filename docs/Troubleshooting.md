## Troubleshooting

**Error Reading Config**

Try removing the config file `$ rm ~/.shallow-backup` and running the program again. Config files from below version 2.0 are incompatible with the config files used after.

**Missing Files After Changing Backup Path**

Don't worry! They'll all be in the git repo, which was moved to the new path. The only exception will be any files that were not under git version control.

Try to `cd` into the backup directory and run `$ git log`. Then you can grab the last commit hash and checkout that revision. Your files will be there.
