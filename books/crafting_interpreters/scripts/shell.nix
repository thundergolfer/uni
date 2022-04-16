{ nixpkgs ? import ./nixpkgs.nix { config = {}; overlays = []; } }:
with nixpkgs;
stdenv.mkDerivation {
  name = "dart-env";

  buildInputs = [
    dart
    git
  ];
}
