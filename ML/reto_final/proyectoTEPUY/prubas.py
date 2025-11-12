import api.echo as API
import app.echo as APP
from dasboard.echo import ping_dash
from database.echo_db import ping

def ejemplo1():
    print(API.ping())
    print(APP.ping())
    print(ping_dash())
    print(ping())
    pass

if __name__ == '__main__':
    ejemplo1()