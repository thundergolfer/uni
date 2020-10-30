{ nixpkgs ? import ./nixpkgs.nix {} }:
with nixpkgs;
nixpkgs.mkShell {
  # this will make all the build inputs from hello and gnutar
  # available to the shell environment
  # I don't actually need those inputs, but I'm keeping them here while still learning Nix.
  inputsFrom = with pkgs; [ hello gnutar ];

  # Directly specify packages I want available in the shell.
  buildInputs = [
    # Useful for option parsing in shell scripts.
    getopt
    # Need to run `git` while in the pure nix-shell
    git
    # Pin Python for (mostly) hermetic Python development in Bazel
    python38
    python38Packages.pip
    python38Packages.virtualenv
    # Useful for avoiding mistakes in Bash scripts
    shellcheck
    which
  ];
}