# myhome
Control RF outlets over a Raspberry Pi with a 433MHz transmitter.
Lots of libraries are already out there to do this, but this makes it all easily configurable with a config file, has a REST API (for future plans to integrate with Amazon Echo), and a light, dynamic web page. The full deployment architecture is also bundled in.

## Install

Install and setup Nginx and Supervisor:
```
sudo apt-get install nginx supervisor
```

Install [wiringPi](http://wiringpi.com/download-and-install/) if needed.

Checkout the repo and install Python dependencies in a virtualenv.
```
cd ~
git clone --recursive https://github.com/evandam/myhome.git
cd myhome
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cd 433Utils/RPi_utils
make
```

Setup to run with supervisor (auto start/restart).
Edit `supervisor.conf` with appropriate paths if different than `/home/pi/myhome`
```
cd /etc/supervisor/conf.d
sudo ln -s ~/myhome/supervisor.conf myhome.conf
sudo supervisorctl reread
sudo supervisorctl update
```

Add the server to Nginx:
```
cd /etc/nginx/sites-available
sudo ln -s ~/myhome/nginx.conf myhome
```

Enable the Nginx site:
```
cd /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/myhome myhome
sudo service nginx restart
```

You should now be able to connect to `http://localhost/`. Replace `localhost` with your Pi's IP address.

# Configure Outlets
Create a Django admin account:
```
cd ~/myhome/mysite
python manage.py createsuperuser
```
Go to `http://localhost/admin` and create new outlets! They'll automatically appear on your home page.

# REST API
Enabled switches can be queried to get their IDs:
```
curl localhost/api/
{"outlets": [{"state": false, "id": 1, "name": "Bedroom Window Light"}, {"state": false, "id": 2, "name": "Living Room Light"}, {"state": false, "id": 3, "name": "Nightstand Light"}]}
```
Switches can then be toggled on or off:
```
curl localhost/api/1/on
{"outlet_name": "Bedroom Window Light", "status": true, "message": "Bedroom Window Light turned on successfully", "outlet_id": 1}
```

You can easily use these commands in crontab or any other automation tool to trigger turning switches on or off.
