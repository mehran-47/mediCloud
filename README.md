## MediCloud
# ToDo in ubuntu:
# $sudo apt-get install apache2
# $chown <username>:<username> -R /var/www/html
# $chmod 755 -R -R /var/www/html
# $cd /var/www/html 
# $git clone https://github.com/mehran-47/mediCloud.git
# Changes in the apache config file located at "/etc/apache2/apache2.conf": add the XML object/notation below.
<Directory /var/www/>
	Options Indexes FollowSymLinks ExecCGI
	AddHandler cgi-script .py
	AllowOverride None
	Require all granted	
</Directory>
# restart apache
# $sudo service apache2 restart