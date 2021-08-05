<h1 align="center"><code>uni'</code></h1>

<!-- The CI badge image won't show in the static site until the repo is public. -->
<p align="center">
    <a href="https://github.com/thundergolfer/uni/actions/">
        <img src="https://github.com/thundergolfer/uni/workflows/CI/badge.svg">
    </a>
</p>


----

A mono-repo containing code I've written or studied for self-education purposes.

## Contents

Currently, the contents of this mono-repo are broken down into the following top-level concerns:

* [**Algorithms**](/algorithms) - Code for Leetcode, mostly.
* [**Books**](/books) - Code for all kinds of practical exercises in various great textbooks. Homework, practicals, exercises, labs, assignments, etc.
    * [Computer Systems: A Programmer's Perspective](/books/computer_systems_app)
    * [Crafting Interpreters](/books/crafting_interpreters)
    * [Data Science From Scratch](/books/data_science_from_scratch)
    * [Functional Programming in Scala](/books/fp_in_scala)  
    * [Programming Rust](/books/programming_rust)
    * [Structure and Interpretation of Computer Programs](/books/sicp)
    * [The Algorithm Design Manual](/books/the_algorithm_design_manual)
    * [The Rust Programming Language](/books/the_rust_programming_language)
* [**Concurrency**](/concurrency) - Code written to learn how to solve concurrency problems/exercises using code.
* [**Databases**](/databases) - SQL, mostly.
* [**Docs**](/docs) - Static-site documentation for monorepo. Served at https://thundergolfer.com/uni, or viewable locally (see readme instructions within folder).
* [**Languages**](/languages) - Code for learning the details of programming languages (C, C++, Java, Python, Rust).
* [**Machine Learning**](/machine_learning) - H Y P E
* [**Performance**](/performance) - Code for learning about how certain programs change in system resource usage under load. 
* [**Operating Systems**](/operating_systems) - Code written to learn how UNIX (Linux, macOS) operating systems actually work.
* [**Optimization**](/optimization) - Code written to learn how to solve optimization problems using code, particularly using the kinds of optimization algorithms used in Machine Learning.
* [**third_party**](/third_party) - Code and configuration for managing third-party code/packages in Bazel, and not of interest in of itself.
* [**Tools**](/tools) - Tooling code, scripts, and configuration, serving the repository's needs and not of interest in of itself.


## Setup

### Prerequisites

1. [Nix](https://nixos.org/) - Provide a hermetic developer environment. Runs properly on my machine, runs properly on everyone else's. At least, that's the idea.
2. [Direnv](https://direnv.net/) - Integrate with Nix's `nix-shell` to provide hermetic developer environment.
3. [`lorri`](https://github.com/target/lorri)
4. [Bazel](https://bazel.build/) - build everything fast, and correctly, no matter the language.
5. [`zstd`](https://github.com/facebook/zstd) - Required during install of Bazel Python toolchain on OSX.

Importantly, the following components are included in the repo's Nix environment specification:

* _Python 3_
* _Racket_ lang, used in [`books/sicp`](/books/sicp)

## Development

### Build

`bazel build //...`

### Test

`bazel test //...`
