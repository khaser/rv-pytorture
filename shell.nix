{ pkgs ? import <nixpkgs> {} }:
let
  rv-toolchain = import ./toolchain.nix { inherit pkgs; };
in
pkgs.stdenv.mkDerivation {
  name = "rv-pytorture";

  buildInputs = with pkgs; [
    # gcc, make and coreutils contained by default
    rv-toolchain
    spike
    verilator
    dtc
    python310
  ];

  src = ./.;
}

