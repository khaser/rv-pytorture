{ pkgs ? import <nixpkgs> {} }:
let 
  sw-toolchain = import ./toolchain.nix { inherit pkgs; };
in
pkgs.mkShell {
  name = "RISC-V hardware develop";

  nativeBuildInputs = with pkgs; [
    sw-toolchain
    spike
    verilator
    dtc
    python310
    (callPackage /etc/nixos/vim.nix { 
      extraRC = ''
        set tabstop=2
        set shiftwidth=2
        '';
    })
  ];
}

