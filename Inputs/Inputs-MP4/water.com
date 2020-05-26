%chk=water.chk
%NProcShared=2
%Mem=2GB
# HF/6-31G(d) geom=check

water energy

0 1
O  -0.464   0.177   0.0
H  -0.464   1.137   0.0
H   0.441  -0.143   0.0
