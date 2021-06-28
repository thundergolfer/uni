<h1 align="center"><code>uni'</code></h1>

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
    * [Structure and Interpretation of Computer Programs](/books/sicp) 🚧
    * [The Algorithm Design Manual](/books/the_algorithm_design_manual)
* [**Concurrency**](/concurrency) - Code written to learn how to solve concurrency problems/exercises using code.
* [**Databases**](/databases) - SQL, mostly.
* [**Docs**](/docs) - Static-site documentation for monorepo. Served at https://uni.thundergolfer.com, or viewable locally (see readme instructions within folder).
* [**Machine Learning**](/machine_learning) - H Y P E
* [**Performance**](/performance) - Code for learning about how certain programs change in system resource usage under load. 
* [**Optimization**](/optimization) - Code written to learn how to solve optimization problems using code, particularly using the kinds of optimization algorithms used in Machine Learning.
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
