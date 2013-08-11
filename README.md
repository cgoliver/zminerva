zminerva
========
Written by zulban. Email zulban@gmail.com for comments. Code quality suggestions are very welcome.

Tired of checking if closed, inactive, or full classes have opened up? This project monitors McGill university's Minerva website and emails you when classes you want have opened up. You just need to provide your Minerva login, an email account, and which courses you want.

###Security
If you're worried about providing your login credentials to a mysterious program (you damn well should be), have a look at the source code first. It's all free and open software.

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

###Usage
At a minimum, you must provide your @mail.mcgill.ca username and password:

	python3 zminerva.py bob.joe@mail.mcgill.ca mcgillpassword

In order to receive emails when course statuses change, you must also provide a recipient email, and a gmail username and password:

	python3 zminerva.py bob.joe@mail.mcgill.ca mcgillpassword bob.joe@hotmail.com robot@gmail.com robotpassword
	
In the case above, we login to Minerva using bob.joe@mail.mcgill.ca. When statuses change, emails are sent to bob.joe@hotmail.com. The emails are sent from robot@gmail.com. For more information, run this:

	python3 zminerva.py -h  

###Statuses
1. Unknown
2. Not active
3. Waitlist is full
4. Waitlist is open
5. Open