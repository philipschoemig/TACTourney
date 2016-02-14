Nginx Deployment
================

- Install [Nginx](http://nginx.org/)
- Install [MySQL](https://www.mysql.com/)
- Install [uWSGI](https://github.com/unbit/uwsgi/) with pip:
```
pip install uwsgi
```
- Create directory /var/www/tactourney
- Place source code into directory /var/www/tactourney/TACTourney
- Copy files nginx.conf and uwsgi.ini into the directory /var/www/tactourney
- Create link to nginx.conf in /etc/nginx/conf.d/tactourney.conf
- Create link to uwsgi.ini in /etc/uwsgi/vassals/tactourney.ini
- Follow the installation and configuration instructions above
- Copy init script uwsgi to /etc/init.d/uwsgi
- Change ownership of directory /var/www/tactourney to nginx user/group
- Change ownership of directory /var/log/uwsgi to nginx user/group
- Start nginx: /etc/init.d/nginx start
- Start uwsgi: /etc/init.d/uwsgi start
