# LabNet Server Stats

````
cp config.json.sample config.json
pip install influxdb psutil fritzconnection elasticsearch
cp deamon.sh /etc/init.d/labnet-logger
chmod +x /etc/init.d/labnet-logger
update-rc.d labnet-logger defaults
````