# PyCache

simple key:value server written with **Python**

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
default is '**127.0.0.1:5521**'

### set memory limit

set an environment variables
```
MAX = size of memory (like 30MB, 8GB)
```
default is '**800MB**'
