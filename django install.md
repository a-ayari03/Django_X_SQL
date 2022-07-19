LINKS :
https://www.rosehosting.com/blog/how-to-install-django-on-centos-7/

### 1/ Update 

    #sudo -i # get sudo privilege
    sudo yum update # update package
    sudo yum install wget`
    yum install zlib-devel`
    
### 2/ Update python package
		sudo yum install python-devel python-setuptools python-pip # installation de python le cas échéant
		sudo pip3 install --upgrade setuptools
		sudo pip install –upgrade pip

### 3/ Install Virtualenv

		sudo pip3 install virtualenv
	
### 4/ Create Virtual Env 
exit sudo privilege first

		cd ~
		virtualenv django # create a new virtual env called Django in home/user/django

### 5/ Install Django in virtualenv 
followed this [stackoverflow](https://stackoverflow.com/questions/55674176/django-cant-find-new-sqlite-version-sqlite-3-8-3-or-later-is-required-found)

		sudo pip install django
		wget https://kojipkgs.fedoraproject.org/packages/sqlite/3.10.0/1.fc22/x86_64/sqlite-3.10.0-1.fc22.x86_64.rpm
		wget https://kojipkgs.fedoraproject.org/packages/sqlite/3.10.0/1.fc22/x86_64/sqlite-devel-3.10.0-1.fc22.x86_64.rpm
		sudo yum install sqlite-3.10.0-1.fc22.x86_64.rpm
		----
		### https://javamana.com/2022/182/202207020012599316.html
		----
		sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-20223 # Installation d'une key ? 
		sudo yum install python3-devel mysql-devel
		pip install mysqlclient
		


### 6/ Create Django project

		cd ~
		source ~/django/bin/activate
		sudo django-admin startproject Dashboard_6SIGMA
	
Create a new Django Project called Dashboard_6SIGMA

### 7/ Start & Launch Project !
		
		source ~/django/bin/activate
		cd Dashboard_6SIGMA
		python3 manage.py migrate
		python3 manage.py runserver 0.0.0.0:8000

### 8 Connect Database to Django
https://www.javatpoint.com/how-to-connect-mysql-to-django
(step 3)
