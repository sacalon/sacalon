echo "$(tput setaf 1)NOTE: This installer is just for UNIX Systems not windows $(tput setaf 3)"
make deps
echo "$(tput setaf 2)* Dependencies where installed ... $(tput setaf 3)"
make build
echo "$(tput setaf 2)* Sacalon was built."
echo "* You can find the Sacalon source app in dist/"
sudo cp ./dist/sacalon /usr/bin/sacalon
echo "* Sacalon was added to path ..."
echo "$(tput setaf 4)To start using sacalon just type command:"
echo "  sacalon filename.sa"
echo "Read the docs here: https://sacalon-lang.github.io/docs/latest/index.html"