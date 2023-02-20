{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        inherit (pkgs)
          mkShell
          python310;

        inherit (pkgs.python310.pkgs)
          transmission-rpc;

        myPython = python310.withPackages (ps: with ps; [ transmission-rpc ]);
      in
      {
        devShell = mkShell {
          buildInputs = [
            myPython
          ];
        };
      }
    );
}
