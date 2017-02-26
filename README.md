# myhome

## Install
Checkout the repository and install Python dependencies in a virtualenv.
```
cd ~
git clone https://github.com/evandam/myhome.git
cd myhome
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install [wiringPi](http://wiringpi.com/download-and-install/)

Install 433Utils:
```
cd ~
git clone --recursive git://github.com/ninjablocks/433Utils.git
cd 433Utils/RPi_utils
make
cd /usr/local/bin
sudo ln -s ~/433Utils/RPi_utils/codesend codesend
sudo ln -s ~/433Utils/RPi_utils/RFSniffer RFSniffer
```

Install and setup Nginx, Gunicorn, and Supervisor:
```
sudo apt-get install nginx gunicorn supervisor
# Run with supervisor
cd /etc/supervisor/conf.d
sudo ln -s ~/myhome/supervisor.conf myhome.conf
sudo supervisorctl reread
sudo supervisorctl update
```

In `/etc/nginx/sites-available/myhome`, paste the following:
```
server {
    listen 80;

    server_name _;

    access_log  /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    location /myhome {
        proxy_pass         http://127.0.0.1:5000/;
        proxy_redirect     off;

        proxy_set_header   Host                 $host;
        proxy_set_header   X-Real-IP            $remote_addr;
        proxy_set_header   X-Forwarded-For      $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto    $scheme;
    }
}
```

Enable the Nginx site:
```
cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/myhome myhome
```
