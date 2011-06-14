"""Static data for EQI
"""

# Template for population legend
# Use string interpolation as follows
# PLTEMPLATE % ((font, fontsize)*4))
PLTEMPLATE = """
H 8 1 Population per square km
D 0 1p
N 2
S 0.3i s 0.2i 223/223/223 0.25p 0.2i
L %s %s L 1-10
S 0.3i s 0.2i 159/159/159 0.25p 0.2i
L %s %s L 10-100
N 2
S 0.3i s 0.2i 96/96/96 0.25p 0.2i
L %s %s L 100-1000
S 0.3i s 0.2i 32/32/32 0.25p 0.2i
L %s %s L 1000-10000
"""

