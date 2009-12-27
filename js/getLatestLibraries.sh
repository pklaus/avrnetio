#!/bin/bash

# when run the first time do:

# cd ~/Downloads/
# git clone git://github.com/sstephenson/prototype.git
# cd -
# cd ~/Downloads/prototype
# rake dist
# cd -
# cp ~/Downloads/prototype/src/prototype.js ./

# and for scriptaculous:

# cd ~/Downloads/
# git clone git://github.com/madrobby/scriptaculous.git
# cd -
# cp ~/Downloads/scriptaculous/src/scriptaculous.js ~/Downloads/scriptaculous/src/builder.js ~/Downloads/scriptaculous/src/effects.js ~/Downloads/scriptaculous/src/dragdrop.js ~/Downloads/scriptaculous/src/controls.js ~/Downloads/scriptaculous/src/slider.js ./


cd ~/Downloads/prototype
git pull origin master
rake dist
cd -
cp ~/Downloads/prototype/src/prototype.js ./

cd ~/Downloads/scriptaculous
git pull origin master
cd -
cp ~/Downloads/scriptaculous/src/scriptaculous.js ~/Downloads/scriptaculous/src/builder.js ~/Downloads/scriptaculous/src/effects.js ~/Downloads/scriptaculous/src/dragdrop.js ~/Downloads/scriptaculous/src/controls.js ~/Downloads/scriptaculous/src/slider.js ./

