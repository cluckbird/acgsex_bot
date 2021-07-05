# Telegram 隨機色圖機器人

### 使用此原始碼的Bot
> 開放的隨機色圖機器人: [@katonei_bot](https://t.me/katonei_bot)

### 已實現的功能
- 爬取每日R18排行榜
- 不夠色！再來一張
- Tag 索引，指定Tag色圖
- 將爬取到的色圖轉為 `WebP` 格式儲存，節省空間

### 需要注意的事件
- 好久之前的怪東西，代碼質量不保證
- 請在使用API前修改 `cookie.conf`，將自己的pixiv登錄cookie填入（R-18內容必須登錄才能請求）
- 請啟動 `app.py`, `bot.py` 兩個 python 檔，`app.py` 為 WebAPI，運行於 `8080` 埠
- 定時任務需要外部實現（定時請求指定API）
- 可能不支援 Python 3.6 以前的版本

----

## 使用教程

#### 1. 安裝依賴庫
```bash
pip3 install python-telegram-bot
pip3 install requests
pip3 install web.py
pip3 install pillow
```

### 2. 申請 Bot Token （如果你有token可以跳過這一步）
- 私訊 [@BotFather](https://t.me/BotFather)，申請 Bot Token
- 將申請到的 BotToken 填入 `bot.py` 的第 `7` 行，如 `123456789:IAWUGHIGEBIEGHEJguegvhsig`

#### 3. 啟動 Bot 和 WebAPI
```bash
nohup python3 app.py &
nohup python3 bot.py &
```

#### 4. 手動設定定時任務
- `xxx.xxx.xxx.xxx:8080/api/updateNow` 爬取每日 R-18 排行榜 (一天一次)
    - 返回值：`ok`
- `xxx.xxx.xxx.xxx:8080/api/tagsdb_update` 更新tag索引列表 (每次爬取/更新圖庫完成後)
    - 返回值：`ok`
- `xxx.xxx.xxx.xxx:8080/api/list_update` 更新全局索引列表 (每次爬取/更新圖庫完成後)
    - 返回值：`ok`

#### 5. 結束！導入色圖庫或開始爬取
- 關於命令：請發送 `/help` 給Bot查看如何操作
- 導入色圖庫：**我將會在整理完成已有的色圖庫後將其上載**

----

### 完整API列表
- `xxx.xxx.xxx.xxx:8080/api/num` 獲取隨機 imgid ( `/webp/` 目錄內的索引)
    - 返回值：隨機imgid，如 `19852`
- `xxx.xxx.xxx.xxx:8080/api/num_tag?tag=tag名` 指定 Tag 的隨機 imgid (需要先更新tag索引列表)
    - 返回值：隨機imgid
- `xxx.xxx.xxx.xxx:8080/api/updateNow` 爬取每日 R-18 排行榜
    - 返回值：`ok`
- `xxx.xxx.xxx.xxx:8080/api/tagsdb_update` 更新tag索引列表
    - 返回值：`ok`
- `xxx.xxx.xxx.xxx:8080/api/list_update` 更新全局索引列表
    - 返回值：`ok`