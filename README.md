<h1 align="center"><code>uni'</code></h1>

<p align="center">
    <a href="https://github.com/thundergolfer/uni/actions/">
        <img src="https://github.com/thundergolfer/uni/workflows/CI/badge.svg">
    </a>
</p>


----

A mono-repo containing code I've written to educate myself. 

## Contents

Currently, the contents of this mono-repo are broken down into the following top-level concerns:

* [**Books**](/books) - Code for all kinds of practical exercises in various great textbooks. Homework, practicals, exercises, labs, assignments, etc.
    * [Computer Systems: A Programmer's Perspective](/books/computer_systems_app)
    * [Structure and Interpretation of Computer Programs](/books/sicp) 🚧
* [**Concurrency**](/concurrency) - Code written to learn how to solve concurrency problems/exercices using code.
* [**Optimization**](/optimization) - Code written to learn how to solve optimization problems using code, particularly using the kinds of optimization algorithms used in Machine Learning.
* [**Tools**](/tools) - Tooling code, scripts, and configuration, serving the repository's needs and not of interest in of itself.


## Setup

### Prerequisites

1. [Nix](https://nixos.org/) - Provide a hermetic developer environment. Runs properly on my machine, runs properly on everyone else's. At least, that's the idea.
2. [Direnv](https://direnv.net/) - Integrate with Nix's `nix-shell` to provide hermetic developer environment.
3. [`lorri`](https://github.com/target/lorri)
4. [Bazel](https://bazel.build/) - build everything fast, and correctly, no matter the language.

Importantly, the following components are included in the repo's Nix environment specification:

* _Python 3_
* _Racket_ lang, used in [`books/sicp`](/books/sicp)

## Development

### Build

`bazel build //...`

### Test

`bazel test //...`
