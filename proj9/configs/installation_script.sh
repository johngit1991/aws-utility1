#!/bin/sh
# remote path location
source '/tmp/configs/installation_data.config'
sudo yum update -y
#Docker installation
printf  "%b\n" "-----------------------------Step1: Docker Installation started--------------------------------------"
printf  "%b\n"
sudo amazon-linux-extras install docker -y
sudo systemctl enable docker.service
sudo systemctl start docker.service
sudo usermod -a -G docker ec2-user
sudo chmod 666 /var/run/docker.sock
printf "%b\n" "-------------------------------Docker Installation completed. !!......................................"
printf  "%b\n"
#prometheus installation
printf  "%b\n" "------------------------------Step2: Prometheus Installation started--------------------------------"
printf  "%b\n"
sudo useradd --no-create-home --shell /bin/false prometheus
sudo mkdir -p /etc/prometheus
sudo mkdir -p /var/lib/prometheus
sudo chown prometheus:prometheus /var/lib/prometheus
cd /tmp/
wget $prometheus_download_url
# wget https://github.com/prometheus/prometheus/releases/download/v2.7.1/prometheus-2.7.1.linux-amd64.tar.gz
tar -xvf prometheus-2.7.1.linux-amd64.tar.gz
cd prometheus-2.7.1.linux-amd64
sudo mv console* /etc/prometheus
sudo mv prometheus.yml /etc/prometheus
sudo chown -R prometheus:prometheus /etc/prometheus
sudo mv prometheus /usr/local/bin/
sudo mv promtool /usr/local/bin/
sudo chown prometheus:prometheus /usr/local/bin/prometheus
sudo chown prometheus:prometheus /usr/local/bin/promtool
sudo chown -R $USER:$USER /etc/systemd/system/
printf "%b\n" "--------------------------updating prometheus.service file---------------------------"
printf  "%b\n"
sudo cat >> /etc/systemd/system/prometheus.service <<EOL
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus --config.file /etc/prometheus/prometheus.yml --storage.tsdb.path /var/lib/prometheus/ --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
EOL
printf  "%b\n" "----------------------------------------Prometheus.service file updation has been completed.--------------------------------------------------"
sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus
sudo systemctl status prometheus
printf  "%b\n" "----------------------------------------Prometheus Installation completed. !!-------------------------------------------------------------------"