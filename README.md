Cardgame
====

Cardgame specification

## Description

## Requirement
Python3

## Usage
card image size 600 x 800

### Cardgame (tested by Python3.7)
sudo pip3 install Flask  
sudo pip3 install names  
sudo apt install sqlite3  
sudo pip3 install Pillow  
sudo pip3 install flask-restx  
cd cardgame/flask  
python3 ./initialize_db.py  
A  
wget https://capybaradino.mydns.jp/resources.tgz  
tar zxvf resources.tgz  
./reset_game.sh  

### Cardgame for production mode
[Note] need edit cardgame.service for your environment  
sudo pip3 install uwsgi  
sudo ln -s /home/pi/cardgame/cardgame.service /etc/systemd/system/  
sudo ln -s /home/pi/cardgame/cardgame_api.service /etc/systemd/system/  
sudo systemctl daemon-reload  
sudo systemctl enable cardgame  
sudo systemctl enable cardgame_api  
sudo cp /home/pi/cardgame/logrotate_cardgame.service /etc/logrotate.d/  

### Cardgame for production mode bot setting
sudo ln -s /home/pi/cardgame/cardgame_bot.service /etc/systemd/system/  
sudo systemctl enable cardgame_bot  

## Debug
To skip user authentication, create file below in the same directory with main.py  
Then, open two browser window. (Note: need using secret mode to use cookies individualy)  
Access as follows:  
  Player1 - http://127.0.0.1:5000/p1  
  Player2 - http://127.0.0.1:5000/p2  

debug.conf
```
[debug]
email1 = user1@example.com
email2 = user2@example.com
email3 = user3@example.com
# p1hp = 5
# p2hp = 5
# p1mp = 7
# p2mp = 7
# p1hp = 15
# p2hp = 15
p1hp = 25
p2hp = 25
p1mp = 0
p2mp = 0
senkou = 1
turntimeout = 125
# p1_topcard0 = meraghost
# p1_topcard1 = obake-candle
# p1_topcard2 = baaru-zebubu
p1_topcard0 =
p1_topcard1 =
p1_topcard2 =
# p2_topcard0 = molly
# p2_topcard1 = killer-pickel
# p2_topcard2 = jaguar-mage
p2_topcard0 =
p2_topcard1 =
p2_topcard2 =
p1_deck = gamecard_wiz_2018haru_3_aguzesi
# p2_deck = gamecard_wiz_2018haru_3_aguzesi
p2_deck = gamecard_mnk_2018haru_2_butoka
```

## Contribution

## Licence

## Author
