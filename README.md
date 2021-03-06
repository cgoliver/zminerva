zminerva
========
## Update: April 2016
The McGill Minerva system was updated in April 2016. This bot has served us well... but it is now broken. At the time of writing, I only have one McGill class left, so this repository probably won't be updated.

## Summary
Tired of checking if closed, inactive, or full classes have opened up? This project monitors McGill university's Minerva website and emails you when classes you want have opened up. You just need to provide your Minerva login, an email account, and which courses you want.

Code quality suggestions are very welcome.

## Security
If you're worried about providing your login credentials to a mysterious program (you damn well should be), have a look at the source code first. It's all free and open software.

## Disclaimer
By default, the check interval is set to 30 minutes. That's recommended. I request that you do not spam McGill by setting this any lower. Plus, you will be blocked if you query too often. Follow the rules in the [Responsible Use of McGill Information Technology Resources](http://www.mcgill.ca/secretariat/sites/mcgill.ca.secretariat/files/Responsible-Use-of-McGill-IT-Policy-on-the.pdf).

This program does not actually register you for classes. That's on you. Automatic class registering and dropping would be really easy to set up, but I figured it's probably best not to mess with that.

## Installation
Requires python 3, lxml, requests, charade and git.

### Linux (Ubuntu)
Install dependencies: 

	sudo apt-get install python3.3 python3-lxml python3-requests git 

Install charade. First, [download it here](https://pypi.python.org/packages/source/c/charade/charade-1.0.3.tar.gz). Extract the folder, navigate to it, and type:
	
	sudo python3 setup.py install

Navigate to where you want the scripts, and get the zminerva project from github:

	cd ~/
	git clone https://github.com/Zulban/zminerva

### Windows
Install steps are a little tedious at the moment, but it's tested. Hopefully you know what a command prompt is. And whether your computer is 32 bit or 64 bit so you know which installers to pick.

[Install Git](http://git-scm.com/downloads).

[Install Python 3.3](http://www.python.org/download/releases/3.3.2/).

[Install lxml for Python 3.3](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml).

[Install requests for Python 3.3](http://www.lfd.uci.edu/~gohlke/pythonlibs/#requests).

Install charade. First, [download it here](https://pypi.python.org/packages/source/c/charade/charade-1.0.3.tar.gz). Extract the folder. Run command prompt. Navigate to the folder, and type:
	
	python setup.py install

Open git bash/terminal/console. Navigate to where you want the scripts, and get the zminerva project from github:
	
	cd c:/
	git clone https://github.com/Zulban/zminerva

### OSX
Untested, but it should almost definitely work if you install the correct packages.

## Usage
### Watch List
The list of courses you want to monitor must be saved in a file named "watchlist". If you run zminerva.py without a watchlist, it will generate a demo watchlist for you. Example:

	fall 2013, comp 250, crn 827
	fall 2013, edpe 335
	
This will monitor the status of only one comp 250 (with that CRN). It also monitors all EDPE 335 and reports only the best status. Use commas and spaces as shown above.  

### Basic
At a minimum, you must provide your @mail.mcgill.ca username and password:

	python3 zminerva.py bob.joe@mail.mcgill.ca mcgillpassword
	
### Full
In order to receive emails when course statuses change, you must also provide a recipient email, and a gmail username and password:

	python3 zminerva.py bob.joe@mail.mcgill.ca mcgillpassword bob.joe@hotmail.com robot@gmail.com robotpassword

Here zminerva logs in to Minerva using bob.joe@mail.mcgill.ca. When statuses change, emails are sent to bob.joe@hotmail.com. The emails are sent from robot@gmail.com.

## Statuses
1. Not active
2. Waitlist is full
3. Waitlist is open
4. Open
5. Overbooked
6. Unknown
7. Not found

## Help
For more options:

	python3 zminerva.py -h
	
I'm also more than happy to help with setup so long as you've already genuinely tried. Just send me an email.   
