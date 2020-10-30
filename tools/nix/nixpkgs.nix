let
  nixpkgs = builtins.fetchGit {
    url = "https://github.com/NixOS/nixpkgs.git";
    rev = "e4d0e33f36491a0e08a3b1a15db13366d7d0785f";
  };
in
import nixpkgs

