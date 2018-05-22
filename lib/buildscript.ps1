$true_python = ""
$python_version= python3 --version
echo $python_version
$python_alternate = python --version
$python_version_desired="Python 3.6.5"
If($python_version_desired -eq $python_version){
  $true_python= "python3"
}
ElseIf($python_alternate -eq $python_version_desired){
  $true_python="python"
}
Else{
  echo "Python 3 not installed"
  echo "Please install Python 3 prior to attempting to build this package."
  exit
}



#Unpackage the geckodriver and the selenium modules
echo "Unpacking Selenium and Chrome"
#7z x selenium-3.11.0.tar.gz selenium-3.11.0
7z x "selenium-3.11.0.tar.gz" -o"selenium-3.11.0"
7z x "selenium-3.11.0\dist\selenium-3.11.0.tar"
Expand-Archive chromedriver_win32.zip
$current_dir = Convert-Path .
setx PATH "$env:path;$current_dir\chromedriver_win32"
#sudo mv geckodriver /usr/local/bin/geckodriver
echo "Installing Selenium"
cd "selenium-3.11.0"
iex "$true_python setup.py install"
