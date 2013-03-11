Office Mood Meter:
==================

Python application that helps co workers decide when to go out for lunch .

* Server side : Python [Bottle](http://bottlepy.org/) with websocket support .
* Client side : Data vizualization [d3.js](http://d3js.org/) , Websockets for live updates .


### Dependencies :
```
pip install bottle gevent bottle-websocket
```

To install gevent you may need to statisfy some dependencies :
```
apt-get install python-dev libevent-dev
```

### Use :
* To add/remove users , edit `config/users.json` file .

I am running the server with cron job that restarts it every midnight . User list is
cleared and count starts again with the new users connecting .
That way i know who is back at work today and who is staying home .

```
crontab -e
00 00 * * * /usr/bin/pkill -f omm.py; python /path/to/omm.py & &>/dev/null
 ```
