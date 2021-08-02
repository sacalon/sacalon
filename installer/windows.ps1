<#
  The windows installer for the hascal
  programming language

  Please set the execution policy to unrestricted
  before running the program
#>

<#
Check the requirements and install packages
and then build the source into an executable
#>
function InstallRequirements {
	python --version
	pip --version
	
	Write-Host "Installing some packages" -Foreground green
	pip install pyinstaller
	Write-Host "Building" -Foreground green
	git clone https://github.com/hascal/hascal.git hascal
	cd hascal/src
	pyinstaller --noconfirm --onefile --console --name "hascal"  "hascal.py"
	Write-Host "Build sucessufully finished" -Foreground green
}

try
{
    git | Out-Null
   "Git is installed"
   InstallRequirements
}
catch [System.Management.Automation.CommandNotFoundException]
{
    Write-Host "An error occured" -ForegroundColor red
}