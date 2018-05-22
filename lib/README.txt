All:
Assumes:
-Chrome is installed (If needed, can be pushed into this build script)
-Python 3 is installed (CANNOT be put into this build script)

*********************************************************
WINDOWS USERS:
You must run the buildscript.ps1 file in an administrator powershell.
The build scripts add all the proper paths to the environment for the chromedriver to work,
so as long as the extracted file stays in place, it doesn't matter where it gets extracted (let the build script 
do its work).

Currently the windows build script does not allow for installation into a virtual environment. I will fix this 
soon.

Assumes:
-Build script assumes 7zip is installed (may be included in the future).
*********************************************************
LINUX USERS:
You must run the buildscript.sh file in the terminal. It will ask for a root password at one point. This can
be run in the following ways:
	 ./buildscript 
		-Installs selenium for the whole system. If this doesn't matter, use this option
		-If two python interpreters are installed on the system, the TestSuite must be run with the python3 command.
		
	 ./buildscript -v <virtualenvdirectory>
	 	-creates a virtual environment to work in with a python3 interpreter being the only one in the environment.
	 	-TestSuite can be run with normal python command
	 	-Need to activate the virtual environment with source /<virtual environment directory>/local/bin/activate
