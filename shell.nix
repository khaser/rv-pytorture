{ pkgs ? import <nixpkgs> {} }:
let 
  sw-toolchain = import ./toolchain.nix { inherit pkgs; };
in
pkgs.mkShell {
  name = "RISC-V hardware develop";

  nativeBuildInputs = with pkgs; [
    # pkgs.pkgsCross.riscv32-embedded.gcc
    sw-toolchain
    spike
    dtc
    jdk # for rics-V torture
    verilator
    python310
    (callPackage /etc/nixos/vim.nix { 
      extraRC = ''
        set tabstop=2
        set shiftwidth=2
        '';
    })
  ];
}

