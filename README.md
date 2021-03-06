# RosettaCircuit
## First program in Python
This program read an "ASCII circuit", a text file representing an electrical circuit, and outputs a LaTeX file
using [CircuiTikz](https://github.com/mredaelli/circuitikz). There are plans to also output SPICE configuration files.

# Example:
We want to go from this:
```
    V1--R1---+---R2--+
             |       |
             |       |    
             m       |    
              OPAMPo-+--V0
             p
             |
             G2
```

to this

![Inverting Op Amp](https://github.com/f-forcher/RosettaCircuit/blob/master/OpAmpImage.png)

# Example usage
From terminal
```
cd project_folder/
python3 src/rosetta.py Test1
```

# Status
The parser of the ASCII graph is finished (apart from the occasional bug) and it creates an adjacency list of classes Component, which in turn contains
the list of other components connected to them. Now we have to write down this list in CircuiTikz or SPICE format.

As for now, the code is quite messy and needs to be refactored (which was to be expected since i made this project also to learn best Python practices).
