---
---
## _Malloc_ Lab

> 👋️ **Note:** Updated to Y86-64 for CS:APP3e. Students are given a small default Y86-64 array copying function and a working pipelined Y86-64 processor design that runs the copy function in some nominal number of clock cycles per array element (CPE). The students attempt to minimize the CPE by modifying both the function and the processor design. This gives the students a deep appreciation for the interactions between hardware and software.

> **Note:** The lab materials include the master source distribution of the Y86-64 processor simulators and the Y86-64 Guide to Simulators. (_I unzipped it into `tar/`_)

## Contents

- Files downloaded from CS:APP website as `archlab-handout.tar`, and listed below in the original README contents

## Lab Assignment Write-Up

[csapp.cs.cmu.edu/3e/malloclab.pdf](http://csapp.cs.cmu.edu/3e/malloclab.pdf).

This write-up is pretty helpful for even those doing self-study. Read through it to learn how to approach this lab's problem.

## Original `README.md`

This section is copied from [csapp.cs.cmu.edu/3e/README-archlab](http://csapp.cs.cmu.edu/3e/README-archlab).
It was modified only to conform to standard Markdown formatting.

It is not particularly useful for people doing self-study, but is reproduced here anyway.

---

```
#####################################################################
# CS:APP Malloc Lab
# Directions to Instructors
#
# Copyright (c) 2002, R. Bryant and D. O'Hallaron, All rights reserved.
# May not be used, modified, or copied without permission.
#
######################################################################
```

This directory contains the files that you will need to run the CS:APP
malloc lab, which develops a student's understanding of pointers,
system-level programming, and memory managment.

### 1. Overview

In this lab, students write their own storage allocator, in particular
implementations of the malloc, free, and realloc functions. A
trace-driven driver (mdriver) evaluates the quality of the student's
implementation in terms of space utilization and throughput.

### 2. Files

- `Makefile`		Makefile that builds the Lab
- `README`			This file
- `grade/`			Autograding scripts
- `malloclab-handout/`	The files handed out to the students
- `src/`			The driver sources
- `traces/`			The malloc/free/realloc trace files used by the driver
- `writeup/`		The malloc lab writeup	

### 3. Building the Lab

Step 1: Configure the driver in `src/` for your site. See `src/README` for
detailed information on the driver.

Step 2: Modify the Latex writeup in `writeup/` to reflect the handout
and handin directions for your site. If you don't use Latex, use your
favorite document preparation system to prepare Postcript and PDF
versions of the writeup in `malloclab.ps` and `malloclab.pdf`.

Step 3: Modify the `LABNAME` and `DEST` variables in `./Makefile` for your
site.

Step 4: Type "make" to build the `$(LABNAME)-handout.tar` file.

Step 5: Type "make dist" to copy the `$(LABNAME)-handout.tar` file
and the writeup to the distribution directory where the students
will retrieve the lab. 

### 4. Grading the Lab

There are autograding scripts for this lab. See grade/README for
details.