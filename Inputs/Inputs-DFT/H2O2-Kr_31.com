%mem=8GB
%nproc=8
#p wb97xd/aug-cc-PVTz iop(3/107=0250000000) iop(3/108=0250000000) int=ultrafine

TCC

0 1
O   0.0  0.0  0.725
O   0.0  0.0  -0.725
H   -0.7037808063803964  0.5905422150634392  1.0235104165661992
H   0.0  0.9187205947411183  -1.0235104165661992
Kr   0.    R1    0.
 Variables:
 R1 15.0

