    $ server01

    server01:~$ sudo mkdir /opt/mynd

    server01:~$ sudo chown $USER:$USER /opt/mynd

    server01:~$ mkvirtualenv --python=/usr/bin/python3 mynd

    server01:~$ pip install -r requirements.txt

    server01:~$ sudo ln -s /opt/mynd/mynd.service /etc/systemd/system/mynd.service

    server01:~$ sudo ln -s /opt/mynd/mynd.socket /etc/systemd/system/mynd.socket

    server01:~$ sudo systemctl daemon-reload

    server01:~$ sudo systemctl start mynd.service

    server01:~$ sudo systemctl status mynd.service
