# CSRF-tutorial 📝

Use Django To Introduce CSRF and Cookies , Session 📝

* [Youtube Tutorial](https://youtu.be/J075bvFA5-Q)

## 前言

大家在看這篇文篇時，建議先看我之前的 [Same-Origin Policy and CORS Tutorial 📝](https://github.com/twtrubiks/CORS-tutorial)，

因為這篇文章算是 [Same-Origin Policy and CORS Tutorial 📝](https://github.com/twtrubiks/CORS-tutorial) 的後續介紹，建議大家有

空的話先看一下 :smile:，本篇文章我將會說明 CSRF 並且透過 [Django](https://github.com/django/django) 簡單實作介紹，也會

順便帶大家認識  Cookies 和 Session。

## CSRF

什麼是 CSRF？ 他可以吃嗎  :joy:

CSRF 全名為 Cross Site Request Forgery 也被稱為 One-Click Attack ，又稱 跨站請求偽造，

為什麼我要特別提到 CSRF ？

先來思考一個問題，我們之前有介紹過 [Same-Origin Policy and CORS Tutorial 📝](https://github.com/twtrubiks/CORS-tutorial)，

而且 CORS 預設也是不能跨站存取，那這樣還會有安全上的問題嗎？

答案是有 :flushed: 就是我們現在要介紹的 CSRF :open_mouth:

先說明一下 CSRF 的攻擊行為，使用者（ 受害者 ）在不知情的情況下，被其他網域

借用身份來完成受害者未經同意的 HTTP request（ 也就是偽造出使用者本人發出的

request ）。為什麼會這樣，原因是因為瀏覽器的機制，你只要發送 request 給某個

網域，就會把關聯的 cookie 一起帶上去。如果使用者是登入狀態，那這個 request

當然就包含了他的資訊（ 例如說 session id ），這 request 看起來就像是使用者本

人發出去的。

由於這裡提到了 Cookies 和 Session，不管各位懂不懂，請允許我任性的簡單介紹一下 :stuck_out_tongue_closed_eyes:

## 介紹 Cookies 和 Session

先簡單解釋一下 Cookies 和 Session 的不同，**Cookie 儲存在 client 端，Session 儲存在 server 端。**

### Cookies

最常看到的 Cookie 應用是在填寫表單，大家一定都有在網頁上填寫資料到一半（ 或

曾經填寫過這個表單 ），然後不小心關掉或下一次有再進到同樣的網頁填表單時，他

會幫你自動填入，這就是透過 Cookie 完成。另外一個常見的就是使用者帳號密碼的保

存，下次登入時可以幫你自動填入。

Cookies 的特性:

* Domain specific，只對同一個 domain 起作用。舉個例子，在 *.twtrubiks.com 存入的 cookie，不會出現在 *.not-twtrubiks.com。

* 生命週期，預設為當你關閉瀏覽器時，這些資料就會被刪除，不過，我們可以透過 cookie 的 expires 屬性設定 `max-age` 來決定保存多久後會刪除。

### Session

Session 是搭配 Cookie 的一種技術，Cookie 是在 Client 端建立一個文件用來暫存一些資

料或是網頁的狀態，但因為某些敏感資料存在 Client 端會有安全性問題，就是資料容易被

偽造，因為 Cookie 中的所有資料在 Client 端都可以被修改 ( 雖然也可以透過加密防範 )，

所以一些重要的資料就不適合放在 Cookie 中，而且 Cookie 如果資料太多也會影響傳輸效

率，因此才把敏感資料或狀態儲存在 Server 端，也就是 Session 。

當你瀏覽一個網頁時，Server 端會隨機產生一段字串給你，然後存在你的 Cookie 中，通常

是 session id，當你下一次瀏覽時，Cookie 會帶上 session id，然後經過 Server 端的資料

比對，就知道你是哪個使用者。

Session 儲存方式有下列幾種:

* 記憶體：MemoryStore，適合開發（ development ）時，因為會有 no cross-process caching 的問題。
* Cookie：將 Session 存在 Cookie 中，缺點是會增加傳輸量。
* Cache 快取：常見的有 [Redis](https://redis.io/) 或 [Memcached](https://memcached.org/)，這個方法是比較常見的方法。
* 資料庫：速度比 Cache 慢。( [Django](https://github.com/django/django) 預設是存在 DB 中 )

詳細的 Django Session 可參考 [https://docs.djangoproject.com/en/1.11/topics/http/sessions/](https://docs.djangoproject.com/en/1.11/topics/http/sessions/)

## 使用 Django 介紹 CSRF 攻擊情境

先介紹一下裡面的資料夾

csrf_tutorial_backed 為 backed，run 起來為 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

django_attack_site 為模擬攻擊（ 被加料 ）的網站，run 起來為 [http://127.0.0.1:8002/](http://127.0.0.1:8002/)

我們今天的主角是阿鬼 :satisfied:  阿鬼是一個管理員，管理文章評論是否可以刪除，如下圖

![](https://i.imgur.com/n5PaM90.png)

阿鬼登入了 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)，並且阿鬼**沒登出**網站，

( 登入的部份我借用 **Django admin** 幫我完成 ，我的 帳號/密碼 設定為 twtrubiks/password123 )

溫馨小提醒:heart:

這裡我們先把 csrf_tutorial_backed 裡面內建的防禦機制關閉，也就是先註解掉 MIDDLEWARE 中的

`django.middleware.csrf.CsrfViewMiddleware`，詳細的後面會再做解釋。

阿鬼此時又瀏覽了其他的網站 [http://127.0.0.1:8002/]( http://127.0.0.1:8002/)，這個網頁中包含了惡意注入的 js，

（ 也有可能是一封信或網頁中的一段惡意程式 ）

惡意 js 程式碼如下

```html
<iframe style="display:none" name="csrf-frame"></iframe>
<form action='http://127.0.0.1:8000/delete/' method='POST' target="csrf-frame" id="csrf-form">
    <input type="hidden" name="id" value="69"/>
    <input type="submit" value="submit"/>
</form>
<script>document.getElementById("csrf-form").submit()</script>
```

上面 js 的使用方法以及來源可參考 [example-of-silently-submitting-a-post-form-csrf](https://stackoverflow.com/questions/17940811/example-of-silently-submitting-a-post-form-csrf)

這個 js 很可怕，你不點他，他都會自動幫你送出 :scream:

當阿鬼點了 [http://127.0.0.1:8002/]( http://127.0.0.1:8002/) 之後，阿鬼的某個檔案（ id 為 69）就莫名奇妙的被刪除了，

[http://127.0.0.1:8002/]( http://127.0.0.1:8002/) 只有一個 submit ，就算沒點，資料也被砍了

![](https://i.imgur.com/wlszNK1.png)

我們觀察一下 Cookie，你會發現 sessionid 在裡面，Server 端當然認為你是本人，

所以合理的把檔案砍了

![](https://i.imgur.com/AW4G1MH.png)

但阿鬼根本不知道阿～

我們來確認一下阿鬼的資料還在不在，id 為 69 的資料的確被砍了

![](https://i.imgur.com/aZaprXU.png)

這也是為什麼 CSRF 會被叫做 One-Click Attack 的關係，甚至可以讓你連點都不用點，

你的資料就不知不覺的消失了 :scream:

## 防範 CSRF 攻擊

剛剛介紹了 CSRF 的攻擊行為，大家一定覺得很可怕 :grimacing:

但其實不用太擔心，也是有防範的方法 :relaxed:

現在大部分的 Framework 都有內建防禦 CSRF 的功能，要開啟也非常簡單。

像是在 Django 中的 MIDDLEWARE 裡就有防禦機制

```python
 MIDDLEWARE = [
    ......
    'django.middleware.csrf.CsrfViewMiddleware',
    ......
]
```

我們剛剛在前面模擬 CSRF 攻擊成功，就是將 `django.middleware.csrf.CsrfViewMiddleware` 註解掉，

詳細原理以及步驟可參考 [https://docs.djangoproject.com/en/1.11/ref/csrf/](https://docs.djangoproject.com/en/1.11/ref/csrf/)

如果把這個打開 ( Django 預設也是開啟的，而且不建議關閉 ) ，就可以成功

阻擋 CSRF 攻擊，如果你再試一次剛剛的流程，這次你會發現資料沒有被刪

除，並且透過 Server 端 Console 看到 CSRF token missing or incorrect （ 403 ）

![](https://i.imgur.com/X5dvCc1.png)

題外話，那使用者該如何保護自己避免 CSRF 攻擊呢 ？

最簡單的就是每次使用完網站就登出，這樣就可以避免掉 CSRF，

不過也不能把避免 CSRF 的攻擊，都交給使用者防範，因為我知道

大家都和阿鬼一樣很懶不喜歡登出 :kissing:

所以，Server 的防範（雖然很簡單）還是要做好 :grinning:

如果看到這邊你還是不太了解，建議可以參考影片 [Youtube Tutorial](https://youtu.be/J075bvFA5-Q)

## 結論

這次透過 [Django](https://github.com/django/django) 介紹 CSRF，相信大家以後聽到這個名詞一定不陌生了，其實，多數框架都有

防禦機制，不用太擔心，但是儘管都有內建防禦機制，我認為還是有必要了解一下什麼是 CSRF

，免得以後看到或被問到的時候，產生了一堆:question::question::question::question:

最後，因為文章內容很多是我去網路上查資料，自己再加以整理的，如果有介紹不清楚或有錯誤

的地方，歡迎大家 issuse 給我，希望大家會喜歡，謝謝大家 :relaxed:

## 執行環境

* Python 3.6.2

## Reference

* [Same-Origin Policy, CORS and CSRF](https://hackmd.io/s/H1cY3TTYe#same-origin-policy-cors-and-csrf)
* [TechBridge-讓我們來談談 CSRF](http://blog.techbridge.cc/2017/02/25/csrf-introduction/)

## License

MIT license
