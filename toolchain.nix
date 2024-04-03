{ pkgs ? import <nixpkgs> {} }:
pkgs.stdenv.mkDerivation rec {
  pname = "syntacore-riscv-toolchain";
  version = "0.1.0";

  src = ../syntacore-toolchain.tar.gz;

  nativeBuildInputs = with pkgs; [
    autoPatchelfHook
    stdenv.cc.cc.lib
    zlib
    ncurses5
    libxcrypt-legacy
  ];

  # buildInputs = nativeBuildInputs;

  sourceRoot = "sc-dt_2022.12-sp1/riscv-gcc/";

  preBuild = ''
    # LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib/:$LD_LIBRARY_PATH";
    addAutoPatchelfSearchPath riscv64-unknown-linux-gnu/lib64/lp64/ sysroot/lib64 sysroot/lib32
  '';

  installPhase = ''
    rm lib/python3.10/lib-dynload/_ctypes.cpython-310-x86_64-linux-gnu.so

    mkdir -p $out/bin
    cp -r ./ $out
  '';

}
