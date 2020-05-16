import twitter
import json
import datetime
import copy

# ツイートからHTMLを作成（関数）
def create_html(text ,username ,userid, tweetid):
  html =  '<blockquote class="twitter-tweet"><p lang="ja" dir="ltr">' + text + '</p>&mdash;' + username +'(@' + userid  +') <a href="https://twitter.com/' + userid + '/status/' +tweetid + '?ref_src=twsrc%5Etfw"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
  return html

# 取得したキーとアクセストークンを設定する(各自のキーを入力)
auth = twitter.OAuth(consumer_key="-------------------",
                     consumer_secret="-------------------",
                     token="-------------------",
                     token_secret="-------------------")

t = twitter.Twitter(auth=auth)

#タイムラインを取得(while文で出来るだけさかのぼる)
date = datetime.datetime.now() # 今の時間の取得
date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=date.hour,minute=date.minute)
count = 0 # 取得ツイートを数えるため
data =[] # 取得したデータを保存
#data_swap =[]
diff = date -date
print("開始時刻",date)

while(1): # データ取得の開始
  if diff.seconds >= 86400 or count >15: #24時間かループの制限に引っかかる時
    print("探索終了")
    print(count)
    break
  elif count ==0: # 一番初めの時
    get_data = t.statuses.home_timeline(count = 200)
    for i in range(len(get_data)):
      # create,"id",name,userid,text,"favorite_count","retweet_count"
      data_swap = [str(get_data[i]["created_at"]),str(get_data[i]["id"]),str(get_data[i]["user"]["name"]),str(get_data[i]["user"]["screen_name"]),str(get_data[i]["text"]),int(get_data[i]["favorite_count"]),int(get_data[i]["retweet_count"])]
      data.append(data_swap)
    last_id = get_data[len(get_data)-3]["id"] # 最後のツイートのidからそれ以前のツイートを取得するようにする
    date_create = get_data[int(len(get_data)-1)]["created_at"]
    date_create_at = datetime.datetime(year=int(date_create[26:30]), month=int(date.month), day=int(date_create[8:10]), hour=int(date_create[11:13]),minute=int(date_create[14:16]))#ツイートの投稿時間の取得
    count = count +1
  else: #それ以外の時
    get_data = t.statuses.home_timeline(count = 800, max_id = last_id)
    if len(get_data) == 0: # 制限にひかかって取得ツイートが0になった時
      print("探索終了")
      break
    for i in range(len(get_data)):
      if i >0: # max_idで指定したツイート以降を取得
        data_swap = [str(get_data[i]["created_at"]),str(get_data[i]["id"]),str(get_data[i]["user"]["name"]),str(get_data[i]["user"]["screen_name"]),str(get_data[i]["text"]),int(get_data[i]["favorite_count"]),int(get_data[i]["retweet_count"])]
        data.append(data_swap)
    last_id = get_data[len(get_data)-1]["id"] # 最後のツイートのidからそれ以前のツイートを取得するようにする
    date_create = get_data[int(len(get_data)-1)]["created_at"]
    date_create_at = datetime.datetime(year=int(date_create[26:30]), month=int(date.month), day=int(date_create[8:10]), hour=int(date_create[11:13]),minute=int(date_create[14:16]))#ツイートの投稿時間の取得
    diff = date -date_create_at
    count = count +1

print("終了時刻",date_create_at)
print("データ総数:",len(data))

# ソートする
size = len(data)
data.sort(key=lambda data: data[5]) #ラムダ式を使ってソートする(ファボ)
data_RT = copy.copy(data)
data_RT.sort(key=lambda data: data[6]) #ラムダ式を使ってソートする(RT)

# 結果の表示(HTML)
path = '/content/drive/My Drive/Colab Notebooks/TwitterAPI/' + 'data/TimeLine' +str(date.month) +'月' +str(date.day) + '日' +'.html'
with open(path, mode='w') as f:
    f.write("<H1>ファボ数が多かったツイートベスト１０！ <H1>")
    f.write("<H1>"+str(date + datetime.timedelta(hours =9)) + "~" +str(date_create_at + datetime.timedelta(hours =9)) +"<H1>")
    for i in range(10):
        f.write("<H2>第"+str(i+1)+"位!!　"+ str(data[size-1-i][5]) + "ファボ <H2>")
        f.write(create_html(data[size-1-i][4],data[size-1-i][2],data[size-1-i][3],data[size-1-i][1]))
        
    # RTの時
    f.write("<H1>RT数が多かったツイートベスト１０！ <H1>")
    for i in range(10):
        f.write("<H2>第"+str(i+1)+"位!!　"+ str(data[size-1-i][6]) + "RT <H2>")
        f.write(create_html(data_RT[size-1-i][4],data_RT[size-1-i][2],data_RT[size-1-i][3],data_RT[size-1-i][1]))
print("書き込み終了")
