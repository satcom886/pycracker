# Badges
![GitHub issues by-label](https://img.shields.io/github/issues-raw/satcom886/rugl/pycracker.svg)
# What can I do with this?
This program can crack MD5 hashes (more hashes comming).
# Usage:
pycracker.py **MaxPasswordLength Hash Characters Hashtype**  
Line 75 can be uncommented in order to print the current candidate (for debugging purposes).
# Possible arguments:
## WARNING: ALL ARGUMENTS MUST BE PRESENT AND HAVE TO BE ENTERED IN THE EXACT ORDER ABOVE!
**MaxPasswordLength** - maximum password length that will be tried  
**Hash** - the hash string  
**Characters** - character sets:  
* "a" means all the letters of the english alphabet (lowercase)
* "A" means uppercase
* "1" means numbers
* "@" means special characters

 **Hashtype** - type of the hash:
* MD5

# Why?
This is a project that aims to create the worlds slowest password cracker. Feel free to hate.

# Any example of what I can do?
Sure! You can try one of these:
1. python pycracker.py 4 79c2b46ce2594ecbcb5b73e928345492 a MD5 *->* **ahoj** *takes almost no time*
4. python pycracker.py 8 1a5e88fec8cde7e4580c554a8d5775d9 1 MD5 *->* **19672324** *takes about 30 seconds*
3. python pycracker.py 10 61e23d859120cbd729bf8dae5898a27b 1 MD5 *->* **1967232454** *takes really long time*
2. python pycracker.py 10 4145b797774ae13c9590a3306e3efc04 aA1 MD5 *->* **Everyth1ng** *even longer*