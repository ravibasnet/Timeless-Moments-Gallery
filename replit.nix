{ pkgs }: {
  deps = [
    pkgs.python311Full
    pkgs.python311Packages.pip
    pkgs.sqlite
  ];
  
  # Install Python dependencies
  shellHook = ''
    pip install -r requirements.txt
  '';
} 