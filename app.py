import web
import requests, re, time, secrets, datetime, os
from PIL import Image

urls = (
    '/(.*)', 'index'
)

class index:
    def GET(self, name):
        web.header('content-type', 'text/html;charset=utf-8', unique=True)
        if name == "api/updateNow":
            # 每日更新
            def get(day):
                try:
                    header = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.75",
                        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "accept-encoding": "gzip, deflate, br",
                        "accept-language": "zh-TW,zh-CN;q=0.9,zh-HK;q=0.8,zh;q=0.7,en-GB;q=0.6,en;q=0.5,en-US;q=0.4:",
                        "referer": "https://pixiv.net",
                        "cookie": str(open("cookie.conf", "r").read())
                    }
    
                    r = requests.get("https://www.pixiv.net/ranking.php?mode=daily_r18&date="+day, headers=header)
                    imglist = re.findall(re.compile(r'i.pximg.net\/c\/240x480\/img-master\/img\/([\s\S]*?)\_p0\_master1200.jpg\"'), r.text)
                    titlelist = re.findall(re.compile(r'data-title\=\"([\s\S]*?)\"'), r.text)
                    userlist = re.findall(re.compile(r'data-user-name\=\"([\s\S]*?)\"'), r.text)
                    tagslist = re.findall(re.compile(r'data-tags\=\"([\s\S]*?)\"'), r.text)
    
                    for i in range(0, len(imglist), 1):
                        try:
                            url = "https://i.pximg.net/img-original/img/" + imglist[i] + "_p0.jpg"
                            img = requests.get(url, headers=header)
                            open("img/"+imglist[i].replace(imglist[i][:20], '')+".png", 'wb').write(img.content)
                            try:
                                json = {}
                                json["title"] = titlelist[i]
                                json["user"] = userlist[i]
                                json["tag"] = tagslist[i]
                                try:
                                    os.mkdir("webp/"+imglist[i].replace(imglist[i][:20], ''))
                                except:
                                    print("圖像 "+imglist[i].replace(imglist[i][:20], '')+" 已存在，跳過請求")
                                    continue
                                im = Image.open("img/"+imglist[i].replace(imglist[i][:20], '')+".png").convert("RGB")
                                im.save("webp/"+imglist[i].replace(imglist[i][:20], '')+"/image.webp", "WEBP")
                                open("webp/"+imglist[i].replace(imglist[i][:20], '')+"/info.json", "w", encoding="utf-8").write(str(json).replace("'",'"'))
                                # print("OK WEBP: "+imglist[i].replace(imglist[i][:20], ''))
                                try:
                                    nownum = open("data/upnum/"+str(datetime.datetime.now().strftime('%Y-%m-%d')), "r").read()
                                except:
                                    open("data/upnum/"+str(datetime.datetime.now().strftime('%Y-%m-%d')), "w").write("0")
                                    nownum = "0"
                                open("data/upnum/"+str(datetime.datetime.now().strftime('%Y-%m-%d')), "w").write(str(int(nownum)+1))
                                print(json)
                            except:
                                print("ERROR: "+imglist[i].replace(imglist[i][:20], ''))
                                os.system("rm -rf webp/"+imglist[i].replace(imglist[i][:20], ''))
                        except:
                            print("ERROR: "+imglist[i].replace(imglist[i][:20], ''))
                            os.system("rm -rf webp/"+imglist[i].replace(imglist[i][:20], ''))
                            
                        secret_generator=secrets.SystemRandom()
                        time.sleep(secret_generator.randint(6, 9))
                except:
                    get(day)    

            now = datetime.datetime.now()+datetime.timedelta(days=-2)
            gettime = (now).strftime("%Y%m%d")
            print("Update："+str(gettime))
            get(gettime)

            return "ok"
        # 隨機色圖 ID（無分類）
        elif name == "api/num":
            imglist = os.listdir(os.getcwd() + "/webp")
            secret_generator=secrets.SystemRandom()
            
            usenum = str(int(open("data/use.conf", "r").read()) + 1)
            open("data/use.conf", "w").write(usenum)
            
            return str(imglist[secret_generator.randint(0, len(imglist)-1)])
        # 隨機色圖ID（有索引，請先生成索引）
        elif name == "api/num_tag":
            try:
                try:tagname = web.input().tag
                except:tagname = ""
                if tagname != "":
                    tagjson = eval(open("data/tags.json", "r").read())
                    secret_generator=secrets.SystemRandom()
                    usenum = str(int(open("data/use.conf", "r").read()) + 1)
                    open("data/use.conf", "w").write(usenum)
                    return str(tagjson[tagname][secret_generator.randint(0, len(tagjson[tagname])-1)])
            except:
                return "error"
        # 生成/更新索引
        elif name == "api/tagsdb_update":
            imglist = os.listdir(os.getcwd() + "/webp")
            try:
                # 讀取tags數據庫
                tagsdb = eval(open("data/tags.json", 'r').read())
            except:
                # 當數據庫讀取失敗（不存在）時創建新的
                open("data/tags.json", 'w').write('{}')
                tagsdb = {}
            # 遍歷色圖列表（取Pixiv ID）
            for i in imglist:
                # 取色圖 info.json
                imginfo = eval(open("webp/"+i+"/info.json", "r").read())
                # 取色圖 info.json 內的 tag，並分割為 list
                tagslist = imginfo['tag'].replace("R-18 ", '').split(" ")
                # 遍歷當前 tag list
                for ii in tagslist:
                    # 創建 / 修改 該tag在數據庫內的訊息
                    tagsdb[ii] = []
            # 第二次遍歷色圖列表（取Pixiv ID）
            for i in imglist:
                # 取色圖 info.json
                imginfo = eval(open("webp/"+i+"/info.json", "r").read())
                # 取色圖 info.json 內的 tag，並分割為 list
                tagslist = imginfo['tag'].replace("R-18 ", '').split(" ")
                # 遍歷當前 tag list
                for ii in tagslist:
                    # 創建 / 修改 該tag在數據庫內的訊息
                    tagsdb[ii].append(i)

            # 更新數據庫
            open("data/tags.json", 'w').write(str(tagsdb).replace("'",'"'))
            return "ok"
        # 更新色圖list檔
        elif name == "api/list_update":
            imglist = os.listdir(os.getcwd() + "/webp")

            open("data/list.json", "w").write(str(imglist).replace("'",'"'))
            return "ok"
        else:
            return "error"

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()