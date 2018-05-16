# Event Management Website:

## Build

* This project is built using HTML, CSS, JavaScript and Python v2.7 languages.
* It is tested on Chrome v61.0 and Firefox v57.0.
* It uses Python Flask framework for server side application.
* It uses Python Sqlalchemy SQL toolkit for database operations in Python.
* It uses Bootstrap 3 for styling.
* It uses jQuery, Popper, Bootstrap JavaScript libraries.

## Instructions

* Start a Vagrant Virtualbox Machine inside the project directory.
* Install <code>python-pip</code>(Python Package Index) to install python frameworks.
* Install <code>flask</code>, <code>sqlalchemy</code> and <code>oauth2client</code> using <code>pip</code>.
* Inside vagrant machine, goto <code>/vagrant</code> directory.
* Run <code>python database_setup.py</code>, <code>python add_data.py</code>, <code>python root.py</code> and <code>python website.py</code> respectively.
* Finally, in your browser, goto <code>localhost:8000</code>, to access the website.

## Dependencies

* Bootstrap v3
* jQuery
* PopperJS
* Flask
* Sqlalchemy
   
## Wiki
* database_setup.py : Code to create and setup the database.
* root.py : Code to add the master account root to the database.
```
    username = root
    password = root
```
* website.py : Code to link the webpages to the database.
* static directory : Contains all CSS, JavaScript, Images and Uploads.
* templates directory : Contains all the HTML webpages.

### Contributers :
Surya Kant Bansal  
E-Mail - skb1129@yahoo.com

Sparsh Rana  
E-Mail - sparshranaazz@gmail.com

Shubham Sharma  
E-Mail - shubham.1997.33@gmail.com

Shubham Jindal  
E-Mail - shubhamjindal1234@gmail.com
