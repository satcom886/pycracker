# pycracker
![GitHub issues](https://img.shields.io/github/issues/satcom886/pycracker)

**Warning**: The program is in it's very early stages. The project aims for compatibility with [Hashtopolis](https://github.com/s3inlc/hashtopolis).  
The documentation below might be outdated and/or inaccurate.  
Most of the code is just a placeholder so that I can focus on making the actual cracking logic. After I have *a* cracker, I will focus on compatibility with Hashtopolis.  
**I *probably* know if the program is completely broken.** There are big changes being made to the code so I won't even attempt to keep a working version for now.

---

here the old readme begins
## What can I do with this?
Right now this program can crack MD5 hashes in a *very slow* and *single-threaded* way.
## Usage:
`pycracker.py` **MaxPasswordLength Hash Characters Hashtype**  
Line 75 can be uncommented in order to print the current candidate (for debugging purposes).
## Possible arguments:
### WARNING: ALL ARGUMENTS MUST BE PRESENT AND HAVE TO BE ENTERED IN THE EXACT ORDER ABOVE!
**MaxPasswordLength** - maximum password length that will be tried  
**Hash** - the hash string  
**Characters** - character sets:  
* "a" means all the letters of the english alphabet (lowercase)
* "A" means uppercase
* "1" means numbers
* "@" means special characters

 **Hashtype** - type of the hash:
* MD5

## Why?
This is a project that aims to create the worlds slowest password cracker. Feel free to hate.

## Any example of what I can do?
Sure! You can try one of these:
1. python pycracker.py 4 79c2b46ce2594ecbcb5b73e928345492 a MD5 *->* **ahoj** *takes almost no time*
4. python pycracker.py 8 1a5e88fec8cde7e4580c554a8d5775d9 1 MD5 *->* **19672324** *takes about 30 seconds*
3. python pycracker.py 10 61e23d859120cbd729bf8dae5898a27b 1 MD5 *->* **1967232454** *takes really long time*
2. python pycracker.py 10 4145b797774ae13c9590a3306e3efc04 aA1 MD5 *->* **Everyth1ng** *even longer*