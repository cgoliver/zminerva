zminerva
========
Written by zulban. Email zulban@gmail.com for comments. Code quality suggestions are very welcome.

Tired of checking if closed, inactive, or full classes have opened up? This project monitors McGill university's Minerva website and emails you when classes you want have opened up. You just need to provide your Minerva login, an email account, and which courses you want.

###Security
If you're worried about providing your login credentials to a mysterious program (you damn well should be), have a look at the source code first. It's all free and open software.

###Disclaimer
By default, the check interval is set to 5 minutes. That's recommended. I suggest you do not spam McGill by setting this any lower.

This program does not actually register you for classes. That's on you. Automatic class registering and dropping would be really easy to set up, but I figured it's probably best not to mess with that.

##Notes
Only does undergrad for now.
Tested with [selenium 2.34.0](https://pypi.python.org/packages/source/s/selenium/selenium-2.34.0.tar.gz)

##Installation
###Linux
Install dependencies: 

	sudo apt-get install python3.3 firefox python3-lxml python3-pip xvfb uchardet 

Use pip to install python libraries:

	sudo pip3 install pyvirtualdisplay selenium

Navigate to "dist-packages" and install ztools:

	cd /usr/lib/python3/dist-packages/
	sudo git clone https://github.com/Zulban/ztools

###Windows and OSX
Currently no Windows or OSX support. Only tested on Linux. It would be really easy to port without xvfb (which allows the --headless option). It's just a matter of using python3-chardet instead of uchardet in ztools/webpage.py.

##Usage
###Monitor List
The list of courses you want to monitor must be saved in the file "watchlist". You must provide a department, code, and semester. CRNs are optional. Example:

	fall 2013, comp 250, crn 827
	fall 2013, edpe 335
	
This will monitor the status of only one comp 250 (with that CRN). It also monitors all EDPE 335 and reports only the best status.  

###Basic
At a minimum, you must provide your @mail.mcgill.ca username and password:

	python3 zminerva.py bob.joe@mail.mcgill.ca mcgillpassword
	
###Full
In order to receive emails when course statuses change, you must also provide a recipient email, and a gmail username and password:

	python3 zminerva.py bob.joe@mail.mcgill.ca mcgillpassword bob.joe@hotmail.com robot@gmail.com robotpassword

###Help
In the case above, we login to Minerva using bob.joe@mail.mcgill.ca. When statuses change, emails are sent to bob.joe@hotmail.com. The emails are sent from robot@gmail.com. For more information, run this:

	python3 zminerva.py -h  

##Statuses
1. Unknown
2. Not active
3. Waitlist is full
4. Waitlist is open
5. Open