from moviepy.editor import *
import os
import praw
import random
from urllib.request import urlretrieve
import magic
if not os.path.isfile(os.getcwd()+"/ytredditconf.txt"):
    with open("ytredditconf.txt","w+") as f:
        print("Hello there! welcome to this.. thing i guess")
        print("basically, you need to input rn your reddit info to get the memes from (yes, its required)")
        f.write(input("now, what is your client id? (get it here https://www.reddit.com/prefs/apps, you can google it to get more info [: ) : "))
        f.write("\n"+input("okk, whats your secret? (not your irl secret) :"))
        f.write("\n"+input("great, now whats your password? (i swer i won't steal it :)) ) :"))
        f.write("\n"+input("your username? :"))
        f.write("\n"+input("and lastly, what sub reddits do you want to see? (separate them by a , ex. cursedimages,blursedimages) :"))

subr = []
with open(os.getcwd()+"/ytredditconf.txt","r") as r:
    l = r.read().splitlines()
    reddit = praw.Reddit(
        client_id=l[0],
        client_secret=l[1],
        password=l[2],
        user_agent="lol",
        username=l[3],
    )
    subr = l[4].split(",")
print(reddit.user.me())
mime = magic.Magic(mime=True)
if input("^ is this you? (Y or n): ") == "n":
    os.remove(os.getcwd()+"ytredditconf.txt")
    exit()
def generatevid(num):
    def get_post():
        l = 0
        if len(subr) >= 1:
            l = random.randint(0,len(subr)-1)
        s = reddit.subreddit(subr[l])
        rand = random.randint(0,   10000)
        ind = 0
        try:
            check = (type(s.random().url))
            sub = s.random()
            data = urlretrieve(sub.url,"out")
            tp = mime.from_file("out")
            if tp in ["image/png", "image/jpeg", "video/mp4"]:
                return [data,tp]
        except AttributeError:
            for sub in s.random_rising():
                data = urlretrieve(sub.url,"out")
                tp = mime.from_file("out")
                if tp in ["image/png", "image/jpeg", "video/mp4"]:
                    return [data,tp]
        return get_post()
    sr = get_post()
    clip2 = VideoFileClip(os.getcwd()+"/input-video.mp4")
    if sr[1] in ["image/png", "image/jpeg"]:
        clip1 = ImageClip(os.getcwd()+"/out",duration=clip2.duration)
    else:
        clip1 = VideoFileClip(os.getcwd()+"/out",duration=clip2.duration,width=1080)
    clip1 = clip1.resize(width=1080)
    x_off = 0
    if clip1.h >= 1280:
        clip1 = clip1.resize(height=1280)
        x_off = (1080-clip1.w)/2


    clip2 = clip2.resize(width=1080)
    audioclip = AudioFileClip(os.getcwd()+"/input-audio.mp3").set_duration(clip2.duration)
    main_clip = CompositeVideoClip([clip1.set_position((x_off,0)),clip2.set_position((0,clip1.h))], size=(1080,1920))
    main_clip.audio =audioclip
    main_clip.write_videofile(os.getcwd()+f'/output/output-video{num}.mp4',fps=25,codec='libx264')
os.mkdir(os.getcwd()+"/output")
for i in range(0,int(input("how many videos should we generate?: "))):
    generatevid(i)