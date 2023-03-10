# sea
**Sea Battle** game by Django

## Types of game
![index](https://drive.google.com/uc?export=view&id=1dZmeaOCCKzyH1KSYPCxTAijjDFEEITwi)
* ### Single player
![play_game](https://drive.google.com/uc?export=view&id=1uyG-A2oiW5G8rZmQt8lfG2c9_PHnAY6r)
![single_play](https://drive.google.com/uc?export=view&id=1FV9r3YGWVl_6GofPVUaRynqoJm7tj5XN)
![score_board](https://drive.google.com/uc?export=view&id=1oHvV2LzrrpJIBlPcYPr5uxdqfDDunQnZ)

* ### Two player 
![search_user](https://drive.google.com/uc?export=view&id=1dZrTvnVw6hL307aCqGM8GlJlv-sJcczZ)
![two_player](https://drive.google.com/uc?export=view&id=1Xd3ZMm-K-UhZnb7xjE9k-lOAoPy9WKC9)
![game_history](https://drive.google.com/uc?export=view&id=1gBI7Uv5Cki92_IqxhbRb-2mxDqk9cOvl)

## Attack Type
### 1.Bomb 
By selecting a cell as a bomb, only that cell is selected
![bomb](https://drive.google.com/uc?export=view&id=1abAXZopIqNSzsupJtlxgnoyzhdz7D3z0) 

### 2.Liner
By selecting a cell as a liner, it moves from the left to the right of the selected row until it hits the ship
![liner](https://drive.google.com/uc?export=view&id=1CeSlK1aKonB1qA1dSwBgvp-kYhNRF4k7)

### 3.Explosion
By selecting a cell  as explosion, the 3x3 area of that cell is selected
![explosion](https://drive.google.com/uc?export=view&id=1T00KFBssBJAJBpRGRe5CsuwPEH1p-TKs)

### 4.Radar
By selecting a cell as a radar, a 3x3 area of that cell's contents (empty or ships) will be displayed.
![radar](https://drive.google.com/uc?export=view&id=1sCYGDKjSn091LMfErXvXN2waTamFHUqz)

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
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```

### Running the code 
Just go into the code directory and type 
```
python manage.py runserver
```
"sea battle game" app will start on 127.0.0.1:8000 (Local Address).
 
enjoy it!

## Task lists
- [x] Add single player
- [x] Add two player (real time) 
- [ ] Add play by bot 
