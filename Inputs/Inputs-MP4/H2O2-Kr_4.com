%mem=2GB
%nproc=2
#p mp4/aug-cc-PVTz int=ultrafine Scan

PTCC

0 1
O   0.0  0.0  0.725
O   0.0  0.0  -0.725
H   0.5905422150634392  0.7037808063803963  1.0235104165661992
H   0.0  0.9187205947411183  -1.0235104165661992
Kr   0.    R1    0.
 Variables:
 R1 3.0 S 20 +0.1

