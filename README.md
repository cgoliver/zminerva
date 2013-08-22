zminerva
========
##Summary
Tired of checking if closed, inactive, or full classes have opened up? This project monitors McGill university's Minerva website and emails you when classes you want have opened up. You just need to provide your Minerva login, an email account, and which courses you want.

Written by zulban. Email zulban@gmail.com for comments. Code quality suggestions are very welcome.

##Security
If you're worried about providing your login credentials to a mysterious program (you damn well should be), have a look at the source code first. It's all free and open software.

##Disclaimer
By default, the check interval is set to 30 minutes. That's recommended. I request that you do not spam McGill by setting this any lower. Plus, you will be blocked if you query too often. Follow the rules in the [Responsible Use of McGill Information Technology Resources](http://www.mcgill.ca/secretariat/sites/mcgill.ca.secretariat/files/Responsible-Use-of-McGill-IT-Policy-on-the.pdf).

This program does not actually register you for classes. That's on you. Automatic class registering and dropping would be really easy to set up, but I figured it's probably best not to mess with that.

On Linux, your credentials will be saved in the bash history. Take precautions.

##Installation

###Linux (Ubuntu)
Install dependencies: 

	sudo apt-get install git python3.3 python3-lxml uchardet 

Navigate to "dist-packages" and install ztools:

	cd /usr/lib/python3/dist-packages/
	sudo git clone https://github.com/Zulban/ztools

Finally, navigate to where you want the scripts, and get the zminerva project from github:
	
	cd ~/
	git clone https://github.com/Zulban/zminerva

###Windows and OSX
Only tested on Ubuntu 13. But Windows and OSX support should be coming soon. I just need to replace ztools.webpage so I can remove uchardet. 

##Usage
###Watch List
The list of courses you want to monitor must be saved in a file named "watchlist". If you run zminerva.py without a watchlist, it will generate a demo watchlist for you. Example:

	fall 2013, comp 250, crn 827
	fall 2013, edpe 335
	
This will monitor the status of only one comp 250 (with that CRN). It also monitors all EDPE 335 and reports only the best status. Use commas and spaces as shown above.  

###Basic
At a minimum, you must provide your @mail.mcgill.ca username and password:

	python3 zminerva.py bob.joe@mail.mcgill.ca mcgillpassword
	
###Full
In order to receive emails when course statuses change, you must also provide a recipient email, and a gmail username and password:

	python3 zminerva.py bob.joe@mail.mcgill.ca mcgillpassword bob.joe@hotmail.com robot@gmail.com robotpassword

Here zminerva logs in to Minerva using bob.joe@mail.mcgill.ca. When statuses change, emails are sent to bob.joe@hotmail.com. The emails are sent from robot@gmail.com.

##Statuses
1. Unknown
2. Not active
3. Waitlist is full
4. Waitlist is open
5. Open

##Notes
Tested with [selenium 2.34.0](https://pypi.python.org/packages/source/s/selenium/selenium-2.34.0.tar.gz).

##Help
For more options:

	python3 zminerva.py -h  