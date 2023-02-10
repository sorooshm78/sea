# sea
**Sea Battle** game by django

![play_game](https://drive.google.com/uc?export=view&id=1uyG-A2oiW5G8rZmQt8lfG2c9_PHnAY6r)

## Attack Type

### 1.Bomb 
by selecting a cell as a bomb, only that cell is selected
![bomb](https://drive.google.com/uc?export=view&id=18Q0n9eBxcpj-evRqkcPscIEwc9nCaQWd) 

### 2.Liner
by selecting a cell as a liner, it moves from the left to the right of the selected row until it hits the ship
![liner](https://drive.google.com/uc?export=view&id=1CRw08ymSxv3FQNhoksanvXbb9cywMs1d)

### 3.Explosion
by selecting a cell  as explosion, the 3x3 area of that cell is selected
![explosion](https://drive.google.com/uc?export=view&id=1Lv4Rv9ydUIUW87XYICzvSdiyv_aLXT0y)

### 4.Radar
by selecting a cell as a radar, a 3x3 area of that cell's contents (empty or ships) will be displayed.
![radar](https://drive.google.com/uc?export=view&id=1W80QWSzNipvIGb_7hOmNnsFNO2-tH-zt)

## Score Board
![score_board](https://drive.google.com/uc?export=view&id=19nwceFB9uGtASCkhQrdPWHRpGypwz8WJ)

## Usage

### With docker
first step clone my project
```
git clone https://github.com/sorooshm78/sea/
```
and then run docker-compose
```
docker-compose up --build
```
"sea battle game" app will start on 0.0.0.0:8000

enjoy it!

### Manually and without docker
I am using python "3.10.6" version 

first step clone my project
```
git clone https://github.com/sorooshm78/sea/
```

and go to app directory and then install requirements  
```
pip install -r requirements.txt
```

this will create all the migrations file (database migrations) now, to apply this migrations run the following command
```
python manage.py makemigrations
python manage.py migrate
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
and you change redis configurations in core/settings.py to:
```
# Cache setting
CACHE_TTL = 15 * 60  # 15 minutes
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

### Running the code 
Just go into the code directory and type 
```
python manage.py runserver
```
"sea battle game" app will start on 127.0.0.1:8000 (Local Address).
 
enjoy it!