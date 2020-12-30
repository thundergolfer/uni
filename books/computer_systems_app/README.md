## _Computer Systems: A Programmer's Perspective_

I worked through this textbook as part of the [teachyourselfcs.com](https://teachyourselfcs.com/) program.

## Contents

1. Twelve `chapter_*` folders containing code the solves the 'homework problems' (and sometimes 'practice problems') from the respective chapter.
2. The `labs/` folder, which contains the 9 labs provided with the CS:APP textbook.

#### "Test your code on multiple machines"

Parts of the textbook (eg. chapter two) are interested in the low-level computer architectural differences between
different machines, like 32-bit vs. 64-bit architectures, and little-endian vs. big-endian.

Homework exercises and practice problems sometimes ask you to "test your code on multiple machines", as if we've all
got multiple computers with different architectures easily accessible.

Below is a table of different platform and whether I've figured how to easily run this repo's code on them:

| **Platform** | **Word Size** | **Endian-ness** | **How To** | **Notes** |
|--------------|---------------|-----------------|------------|-----------|
| Linux 64-bit | 64 | Little | Use [_Github Codespaces_](https://github.com/codespaces) | The `.devcontainer` configures the Github Codespace automatically |
| Linux 32-bit | 32 | Little | 🚧 Dunno yet | |
| OSX 64-bit   | 64 | Little | I use my personal laptop, which is 64-bit by default. | |
| Windows      | 64 | Little | 🚧 Dunno yet | |
| Sun (Solaris)| 64 | Big    | 🚧 Dunno yet | Bazel will not be useable. |