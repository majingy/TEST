#!/bin/bash
python_version="$(python3 --version)"
echo "$python_version"
python_version_desired="Python 3.5.2"


if [[ $1 == "-h" ]]
then
  echo "Usage ./buildscript.sh [flag] [optional]"
  echo "Flags:"
  echo " -v: Create virtual environment using virtualenv. Requires directory name in optional."
  echo " -h: Display help menu"
  exit 0
fi
if [ "$python_version" != "$python_version_desired" ]
then
  echo "Python 3 not installed"
  echo "Please install Python 3 prior to attempting to build this package."
else

  if [[ $1 == "-v" ]] && [[ $# -eq 2 ]]
  then
    #Unpackage the geckodriver and the selenium modules
    echo "Unpacking Selenium and geckodriver"
    tar -xzvf selenium-3.11.0.tar.gz
    unzip -p chromedriver_linux64.zip > chromedriver
    sudo mv chromedriver /usr/local/bin/chromedriver
    sudo chmod +x /usr/local/bin/chromedriver
    python3 -m venv $2
    source $2/bin/activate
    python_version="$(python --version)"
    echo "$python_version"
    echo "Virtual environment instantiated, installing Selenium"
    cd selenium-3.11.0
    python setup.py install
  elif [[ $1 == "-v" ]] && [[ $# -ne 2 ]]
  then
    echo "No target directory for virtual environment."
    echo "Exiting"
    exit 1
  elif [ $# -eq 0 ]
  then
    #Unpackage the geckodriver and the selenium modules
    echo "Unpacking Selenium and geckodriver"
    tar -xzvf selenium-3.11.0.tar.gz
    tar -xvf geckodriver-v0.20.0-linux64.tar.gz -O > geckodriver
    sudo mv geckodriver /usr/local/bin/geckodriver
    echo "Installing Selenium"
    cd selenium-3.11.0
    python3 setup.py install
  else
    echo "Usage ./buildscript.sh [flag] [optional]"
    echo "Flags:"
    echo " -v: Create virtual environment using virtualenv. Requires directory name in optional."
    echo " -h: Display help menu"
    exit 0
  fi


fi

#If so, create the virtual environment and then call pip to install selenium from source
