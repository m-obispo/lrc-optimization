%mem=8GB
%nproc=8
#p lc-wpbe/aug-cc-PVTz int=ultrafine counterpoise=2

TCC

0 1
O(Fragment=1)   0.0  0.0  0.725
O(Fragment=1)   0.0  0.0  -0.725
H(Fragment=1)   0.0  0.9187205947411183  1.0235104165661992
H(Fragment=1)   0.0  0.9187205947411183  -1.0235104165661992
Kr(Fragment=2)   0.    R1    0.
 Variables:
 R1 15.0

