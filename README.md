## Rising Playlist Creator
This is a python script that will copy the playlist that is posted daily on the /r/rising subreddit to your youtube account.  It also has an option to delete it.

## Prerequisites

Clone the project:

    git clone https://github.com/markfaine/rising-playlist-creator
    cd rising-playlist-creator

I can't really offer this as a service because I don't know how to do that and I'd have to pay for all those API hits so you'll have to have a little bit of developer knowledge to set this up.  It requires that you create and configure credentials in Google developer console.

Here is a [video](https://www.youtube.com/watch?v=6bzzpda63H0) that will show you how to do that.  Another [video](https://youtu.be/86YgnJMDrfk) by the same person was the inspiration for this project.  

**NOTE:** Be sure to download the client file to 'client_secret_file.json' to the directory from which you will be running rising-playlist-creator.

Next you will need to create an application on reddit.  Go [here](https://ssl.reddit.com/prefs/apps/) to do that

Edit rising.py and then set the following constants to the respective values in your application on reddit.

```
REDDIT_CLIENT_ID = '<your client id>'
REDDIT_SECRET_KEY = '<your secret key>'
```

## Setup
With the above prerequisites complete you can now install the module.  It's of course best to install into a virtualenv but setting up a virtualenv is definitely out of scope for this readme.

    ```python3 setup.py install``

You should now have the command `rising-playlist-creator`


## Usage
To see the list of options run
```rising-playlist-creator -h
usage: rising-playlist-creator [-h] [--debug] [--delete] [date]

Add a Rising playlist to your Youtube account

positional arguments:
  date        Optional date of the playlist to add, default is today and the format is mm/dd/yy

optional arguments:
  -h, --help  show this help message and exit
  --debug     Enable debug logging
  --delete    Just delete your playlist with this date, if found
```

## Cron
To use this script with cron add something like the following to your crontab:
If ```$HOME/bin``` is where you have saved ```client_secret_file.json```:
```
0 10 * * 1-5 cd "$HOME/bin" && rising-playlist-creator &>/dev/null
0 22 * * 1-5 cd "$HOME/bin" && rising-playlist-creator --delete &>/dev/null
```

## Contributing

Please feel free to fork and make it better


