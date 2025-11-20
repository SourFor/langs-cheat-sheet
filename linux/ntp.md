# NTP

```sh
sudo -i
vi /etc/systemd/timesyncd.conf
```

```ini
NTP=10.15.12.100 10.15.12.200
FallbackNTP=
```

```sh
systemctl restart systemd-timesyncd.service
journalctl -u systemd-timesyncd.service
timedatectl timesync-status
```
