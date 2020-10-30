{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.hello
    # Useful for option parsing in shell scripts.
    pkgs.getopt
    # Need to run `git` while in the pure nix-shell
    pkgs.git
    # Pin Python for (mostly) hermetic Python development in Bazel
    pkgs.python38
    pkgs.python38Packages.pip
    pkgs.python38Packages.virtualenv
    # Useful for avoiding mistakes in Bash scripts
    pkgs.shellcheck
    pkgs.which
    # keep this line if you use bash
    pkgs.bashInteractive
  ];
}
