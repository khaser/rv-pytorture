{ pkgs ? import <nixpkgs> {} }:
pkgs.dockerTools.buildNixShellImage {
  drv = import ./shell.nix {};
  name = "rv-pytorture";
  tag = "latest";
  command = "{ [ -d rv-pytorture ] || unpackPhase; }; /usr/bin/env bash";
}
