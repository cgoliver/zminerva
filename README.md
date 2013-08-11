zminerva
========
Written by zulban. Email zulban@gmail.com for comments. Code quality suggestions are very welcome.

Tired of checking if closed, inactive, or full classes have opened up? This project monitors McGill university's Minerva website and emails you when classes you want have opened up. You just need to provide your Minerva login, an email account, and which courses you want.

If you're worried about providing your login credentials to a mysterious program (you damn well should be), have a look at the source code first. It's all free and open software. 

Statuses are:
"Unknown"
"Not active"
"Waitlist is full"
"Waitlist is open"
"Open"

Installation
========
Only works on Linux (because of uchardet and --headless).

1. This project has some dependencies:
python3.3 firefox python3-lxml python3-pip xvfb uchardet

sudo apt-get install python3.3 firefox python3-lxml python3-pip xvfb uchardet 

cd /usr/lib/python3/dist-packages/
sudo git clone https://github.com/Zulban/ztools

sudo pip3 install pyvirtualdisplay selenium


selenium 2.34.0
https://pypi.python.org/packages/source/s/selenium/selenium-2.34.0.tar.gz