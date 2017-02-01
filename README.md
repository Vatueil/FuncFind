# Funcfind

This IDA script is used for finding Functions in existing binaries.

Relies on NetworkX for calculating subgraphisomorphism.

This script is a prototyp and was written as part of my Bachelor Thesis 2015.

The script exports the control flow graphs  of all functions from IDA and uses subgraphisomorphism to match with templates to find similar functions. It also uses additional information from /helper for more precise matching.

/helper contains descriptions for some architectures.

/templates contains templates for finding functions.

config.py  contains a config

The script was created to speed up reversing of unkown binaries by helping to name functions. Main purpose was for stripped binaries in embedded systems.





