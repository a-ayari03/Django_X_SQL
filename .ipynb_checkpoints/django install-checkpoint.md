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

		source ~/django/bin/activate
		sudo yum install python3-devel mysql-devel
		pip3 install mysqlclient
		


### 6/ Create Django project

		cd ~
		source ~/django/bin/activate
		sudo django-admin startproject Dashboard_6SIGMA
	
Create a new Django Project called Dashboard_6SIGMA

### 7/ Connect Database to Django
FIchier **setting. py** à modifier dans Dashboard_6SIGMA/Dashboard_6SIGMA
		
		DATABASES = {
		    'default': {
		    'ENGINE': 'django.db.backends.mysql',
		    'NAME': 'base6sigma',
		    'USER':'alexandre’,
		    'PASSWORD':'Sigma64ever',
		    'HOST':'localhost',
		    'PORT':'3306',
		    }
		}

### 8/ Start & Launch Project !
		
		source ~/django/bin/activate # (si ce n'est pas déja fait)
		cd Dashboard_6SIGMA
		sudo python3 manage.py migrate
		sudo python3 manage.py runserver

## First table

### 1/
https://codeloop.org/django-rendering-data-from-mysql-database/
		
		sudo python3 manage.py startapp indicateur
		sudo chmod a+rwx indicateur/ # change perm for everyone
		sudo chmod 777  indicateur/models.py 
		sudo chmod 777  indicateur/views.py 
 
 ### 2/

schema model 
		
		class indicator_room(models.Model):   
    Month_name = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)
    Total = models.CharField(max_length=100)
    P1_P2 = models.CharField(max_length=100)
    P3_P4 = models.CharField(max_length=100)
    P1 = models.CharField(max_length=100)
    P2 = models.CharField(max_length=100)
    P3 = models.CharField(max_length=100)
    P4 = models.CharField(max_length=100)
    class Meta:
		managed = False
        db_table = "indicator_it_equipment_count_per_type_per_salle"
        
Lorsqu'il y a des changements dans les tables
https://stackoverflow.com/questions/70720876/how-to-create-a-class-and-connect-it-with-an-existing-table-in-django
Avec le managed = False et le migrate --fake Django comprend que les table existe déja
		 sudo python3 manage.py makemigrations
		 sudo python3 manage.py migrate --fake


