# PyCache

simple key:value server written by **Python**

and client is [here](https://github.com/chick0/pycache_client/)


## run server
```commandline
python -m pycache.server
```

or

```python
from pycache.server import start_server

start_server()
```


### set custom Host and Port

set an environment variables
```
HOST = your ip (like 127.0.0.1, 0.0.0.0)
PORT = your port
```
