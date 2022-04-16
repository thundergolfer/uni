let
  nixpkgs = fetchTarball {
    url = "https://github.com/nixos/nixpkgs/archive/0ecf7d414811f831060cf55707c374d54fbb1dec.tar.gz";
    # Hash is obtained using `nix-prefetch-url --unpack <url>`
    sha256 = "00xbm9lrivsj2w1jks2cnk5brbg5kvxjfj23kq0qyr8nvh57wln9";
  };
in
  import nixpkgs
