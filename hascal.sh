echo "$(tput setaf 1)NOTE: This installer is just for UNIX Systems not windows $(tput setaf 3)"
make deps
echo "$(tput setaf 2)* Dependencies where installed ... $(tput setaf 3)"
make build
echo "$(tput setaf 2)* Hascal was built..."
echo "* You can find the Hascal source app in dist/"
sudo cp ./dist/hascal /usr/bin/hascal
echo "* Hascal was added to path ..."
echo "$(tput setaf 4)To start using hascal just type command:"
echo "  hascal filename.has"
echo "Read the docs here: https://hascal.github.io/docs/latest/index.html"