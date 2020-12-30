<h1 align="center"><code>uni'</code></h1>

<p align="center">
    <a href="https://github.com/thundergolfer/uni/actions/">
        <img src="https://github.com/thundergolfer/uni/workflows/CI/badge.svg">
    </a>
</p>


----

A mono-repo containing code I've written to educate myself. 


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