# Twitter Video Song Finder Bot
Ever been in a situation where you saw a video with a banger song but didn't know its name?
Just [@VideoSongFinder](https://twitter.com/VideoSongFinder) and we'll reply back with the song name :smiley:

![](images/bot-in-action.png)

> Note: This has been tested on Linux/Debian | Ubuntu 20.04 LTS

## **Setup**


### **Requirements and Heroku runtime:**

- ```Python>=3.8.1```
- ``` pip3 ```    *( use pip for python3 if it supports your case )*

To clone the repository use the statement below or any other statement of choice
```bash
git clone https://github.com/chandratop/twitter-song-finder-bot.git
```
In the project repository type the following in the terminal to install all the necessary dependencies
```bash
pip3 install -r requirements.txt
```
---
### **Get API keys**
#### Twitter API
Register for a [Twitter developer account](https://developer.twitter.com/en). Follow the steps to set up your Bot account and get your API keys.
#### ACRCloud API
Register for a [ACRCloud Account](https://docs.acrcloud.com/docs/acrcloud/tutorials/identify-music-by-sound/). Follow the steps to set it up and get your API keys.

---

### **Set API keys**

- Rename the ```.env_sample``` file to ```.env``` 
- Replace ```your-key-here``` the necessary API keys

```
TWITTER_CONSUMER_KEY=your-key-here
TWITTER_CONSUMER_SECRET=your-key-here
TWITTER_ACCESS_KEY=your-key-here
TWITTER_ACCESS_SECRET=your-key-here
ACR_HOST_NAME=your-key-here
ACR_ACCESS_KEY=your-key-here
ACR_ACCESS_SECRET=your-key-here
```

---

### **Minor adjustments** *( Temporary fix )*

Create a fallback tweet and get the ```tweet-id``` from the url.
```
https://twitter.com/user-name/tweet-id
```
Go to [bot.py](https://github.com/chandratop/twitter-song-finder-bot/blob/master/bot.py) and replace the following line as follows.
```
temporary.write("1267382918214643713")

to

temporary.write("tweet-id")
```
