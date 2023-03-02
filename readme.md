# FileMover

![](https://img.shields.io/appveyor/ci/gruntjs/grunt.svg)![](https://img.shields.io/badge/platform-*nix%20%7C%20windows-lightgrey)![](https://img.shields.io/badge/python-3.6%2B-blue)![](https://img.shields.io/badge/license-MIT-orange.svg)

FileMover is a small script that allows you to transfer files between local and mounted repositories and rotate them.

## Arguments

* -s - **(required)** source file for copying or moving

* -t - **(required)** target directory where the file will be placed and rotated

* -f - **(required)** file name in the target directory (during rotation, a postfix like `.N` will be added)

* -l - number of last copies of the file (default: 7)

* -c - copy the original file (not moving it)

* -comp - if the new file matches the last copy, do not add this file to the collection
