# sea
**Sea Battle** game by django

![poster](.github/images/poster.png)

## Attack Type

### 1.Bomb : by selecting a cell as a bomb, only that cell is selected
![bomb](.github/images/bomb1.png) 

### 2.Liner : by selecting a cell as a liner, it moves from the left to the right of the selected row until it hits the ship
![liner](.github/images/liner1.png)

### 3.Explosion : by selecting a cell  as explosion, the 3x3 area of that cell is selected
![explosion](.github/images/explosion1.png)

### 4.Radar : by selecting a cell as a radar, a 3x3 area of that cell's contents (empty or ships) will be displayed.
![radar](.github/images/radar1.png)

## Score Board
![end-game](.github/images/score.png)

### Usage
I am using python "3.10.6" version 

first step clone my project
```
git clone https://github.com/sorooshm78/sea/
```

and then install requirements  
```
pip install -r requirements.txt
```

### Setup Redis Cache 
Install Redis on Linux 
```
sudo apt-get update
sudo apt-get install redis
```
Run the Redis server from a new terminal window.
```
redis-server
```
and you can change redis configurations in core/settings.py
```
# Cash setting
CACHE_TTL = 15 * 60 # 15 minutes
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
```
by default cached for 15 minutes and you change timeout cache
```
CACHE_TTL = 15 * 60
```

### Running the code 
Just go into the code directory and type 
```
python manage.py runserver
```
"sea battle game" app will start on 127.0.0.1:8000 (Local Address).
 
enjoy it!