# myhome
Control RF outlets over a Raspberry Pi with a 433MHz transmitter.
Lots of libraries are already out there to do this, but this makes it all easily configurable with a config file, has a REST API (for future plans to integrate with Amazon Echo), and a light, dynamic web page. The full deployment architecture is also bundled in.

The core application uses Flask to handle API calls and serve a web page. Gunicorn is used to run the application and handle things like worker threads, with supervisor in place to ensure it is always running. Nginx is the public-facing web server.

## Install

Install and setup Nginx, Gunicorn, and Supervisor:
```
sudo apt-get install nginx gunicorn supervisor
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

You should now be able to connect to `http://localhost/myhome`. Replace `localhost` with your Pi's IP address.

# Configure Switches
Edit `switches.conf` by naming the sections as desired and using RF codes that can be found by running `433Utils/RPi_utils/RFSniffer`.
Restart the server to see changes: `sudo supervisorctl reload myhome`

# REST API
Enabled switches can be queried to get their IDs:
```
curl localhost/myhome/api/switch
[{"id": 0, "name": "Living Room Light"}, {"id": 1, "name": "Nightstand Light"}, {"id": 2, "name": "Bedroom Window Light"}]
```
Switches can then be toggled on or off:
```
curl localhost/myhome/api/switch/0/on
{"message": "Living Room Light turned on!", "switch": {"id": 0, "name": "Living Room Light"}, "state": "on"}
```
You can easily use these commands in crontab or any other automation tool to trigger turning switches on or off.
