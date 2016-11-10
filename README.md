ETAG API Docker Build 
===================
Django Rest API which includes Tasks, Catalog, Local Data Store
Docker api works in conjuction with docker cybercom/celery image.


This is a repository that will run with the cybercommons platform.

### Install

* Install Cybercommons Platform [cybercom](https://github.com/cybercommons/cybercom-cookiecutter)
* Then replace the default api_code  folder with this repository.
* Run Docker Build
    $  docker build -t api .
* Adjust config/api_config. Add Database connections

