# twitch-clipper
## A script that creates compilations from the top clips over a period of time from a specific game on Twitch

### How to run
To run the script you'll need to created a file named  `config.py` which will store your Twitch client id, the game id that you want to scrape and where you want to download the clips and export the compilation videos too. 

Config.py example
 ```
 config = {
     'CLIENT_ID': '###',
     'GAME_ID": '###',
     'DOWNLOAD_DIR': '###'
 }
 ```
 
 Then just run main.py and the script will run till completion. On average for 10 clips the script will take 30+min depending on the average length of the clips. 
 
 
 ### Configs
 You could change what period of time the script deals with in function `get_recent_top_clips_data` by changing the params. I'd recommend to check out the Twitch API for this. You can also increase the number of clips you want to download by changing the `first` param in the same function.
 
