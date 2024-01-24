
import sys, os

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

gparent_dir = os.path.dirname( parent_dir )
sys.path.append(gparent_dir)

import utils

from importlib import reload
reload( utils )

print( 'Granny of Home.py: ' + gparent_dir )
print( 'Parent of Home.py: ' + parent_dir )


