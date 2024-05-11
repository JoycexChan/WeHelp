from fastapi import FastAPI, Form, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import mysql.connector
from fastapi.responses import JSONResponse

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="some-random-string")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/signup")
async def signup(request: Request, name: str = Form(...), username: str = Form(...), password: str = Form(...)):
    conn = mysql.connector.connect(
        host="localhost",
        user="websiteuser",
        password="websitepassword",
        database="website"
    )
    cursor = conn.cursor()

    # 檢查用戶名是否已存在
    cursor.execute("SELECT name FROM member WHERE username = %s", (username,))
    member = cursor.fetchone()
    if member:
        cursor.close()
        conn.close()
        message = "Repeated username"
        return RedirectResponse(url=f"/error?message={message}", status_code=status.HTTP_303_SEE_OTHER)
    
    # 用戶名不存在，新增用戶到資料庫
    cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password))
    conn.commit()  # 確認插入操作
    cursor.close()
    conn.close()
    return RedirectResponse(url="/?message=註冊成功", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/signin")
async def show_signin(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#嘗試從 /submitmessage 路由重定向到 /signin 時發生了一個 405 Method Not Allowed 錯誤
#這通常表明試圖以不支持的方法訪問某個路由。在這種情況下，/signin 路由很可能只接受 POST 方法，而您嘗試進行了一個 GET 請求。
#這是一個處理 GET 請求的路由，其主要用途是展示登入頁面。

@app.post("/signin")
async def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    # 建立資料庫連接
    conn = mysql.connector.connect(
        host="localhost",
        user="websiteuser",
        password="websitepassword",
        database="website"
    )
    cursor = conn.cursor()

    # 從資料庫查詢會員名稱
    cursor.execute("SELECT id, name, username FROM member WHERE username = %s AND password = %s", (username, password))
    member = cursor.fetchone()  # 返回的是一個元組或 None
    cursor.close()
    conn.close()

    if member:
        request.session['signed_in'] = True
        request.session['username'] = member[2]  # 存取元組中的 username
        request.session['member_id'] = member[0]  # 存取元組中的 id
        request.session['member_name'] = member[1]  # 存取元組中的 name

        return RedirectResponse(url="/member", status_code=status.HTTP_303_SEE_OTHER)
    else:
        message = "Username or password is not correct"
        return RedirectResponse(url=f"/error?message={message}", status_code=status.HTTP_303_SEE_OTHER)
 
#member資料庫依序 id | name  | username | password  | follower_count | time    
#這是一個處理 POST 請求的路由，用於處理從登入表單提交的數據。
#async def signin(request: Request, username: str = Form(...), password: str = Form(...)):
#這個函數同樣是異步的，適合處理可能包含阻塞性 I/O 操作（如數據庫訪問）的請求。
#username: str = Form(...), password: str = Form(...): 使用 Form() 來從提交的表單中提取 username 和 password 字段。這是 FastAPI 的便利功能，可以直接從表單數據中提取變量。
#數據庫連接和查詢
#mysql.connector.connect(...): 使用 MySQL Connector/Python 建立與數據庫的連接。
#cursor.execute(...): 執行 SQL 查詢，檢查是否存在與提供的 username 和 password 匹配的會員。
#登入成功與否的處理
#如果查詢到會員，則設置會話變量並重定向到會員頁面。
#如果未查詢到，則重定向到錯誤頁面，顯示適當的錯誤信息。
#重定向和會話管理
#request.session['signed_in'] = True 等操作將用戶的狀態存儲在會話中，這對於管理用戶的登入狀態是必需的。
#RedirectResponse(url="/member", status_code=status.HTTP_303_SEE_OTHER): 這個響應將用戶的瀏覽器重定向到 /member 路由，使用 303 狀態碼是為了遵循 POST-重定向-GET 模式，確保用戶刷新頁面時不會重複提交表單。

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    # 建立資料庫連接
    conn = mysql.connector.connect(
        host="localhost",
        user="websiteuser",
        password="websitepassword",
        database="website"
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.content, mem.name, m.like_count, m.time, m.member_id, m.id
        FROM message m
        JOIN member mem ON mem.id = m.member_id
        ORDER BY m.id DESC
    """)
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    if 'signed_in' in request.session and 'member_name' in request.session:
                # 讀取會話中存儲的用戶資訊
        member_id = request.session.get('member_id')
        member_name = request.session.get('member_name')
        username = request.session.get('username')
        return templates.TemplateResponse("member.html", {"request": request, "member_id": member_id, "member_name": member_name, "username": username, "user_id": member_id, "messages": messages})
    else:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


#新增帳密登入website資料庫(websiteuser websitepassword)
#CREATE USER 'websiteuser'@'localhost' IDENTIFIED BY 'websitepassword';
#GRANT ALL PRIVILEGES ON website.* TO 'websiteuser'@'localhost';
#FLUSH PRIVILEGES;
#mysql -u websiteuser -p

@app.post("/submitmessage")
async def submit_message(request: Request, message: str = Form(...)):
    user_id = request.session.get('member_id')  # 假設會話中存有 member_id
    if not user_id:
        return RedirectResponse(url="/signin", status_code=303)  # 如果未登入則重定向到登入頁

    # 連接數據庫
    conn = mysql.connector.connect(
        host="localhost",
        user="websiteuser",
        password="websitepassword",
        database="website"
    )
    cursor = conn.cursor()
    
    # 插入留言數據
    cursor.execute("INSERT INTO message (member_id, content, like_count, time) VALUES (%s, %s, %s, NOW())", 
                   (user_id, message, 0))
    conn.commit()
    cursor.close()
    conn.close()
    
    return RedirectResponse(url="/member", status_code=303)  # 提交後重定向到會員頁

@app.get("/signout")
async def signout(request: Request):
    # 從會話中移除 signed_in 狀態
    request.session.pop('signed_in', None)
    request.session.pop('username', None)  # 移除用戶名
    request.session.pop('member_name', None)  # 移除會員名稱
    # 重新定向到首頁
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# 錯誤頁面
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.post("/deletemessage/{message_id}")
async def delete_message(request: Request, message_id: int):
    # 检查用户是否已登录
    if 'member_id' not in request.session:
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    user_id = request.session.get('member_id')

    conn = mysql.connector.connect(
        host="localhost",
        user="websiteuser",
        password="websitepassword",
        database="website"
    )
    cursor = conn.cursor()

    # 执行联合查询以验证留言所有权
    cursor.execute("""
        SELECT m.id, m.content, m.member_id, mem.name 
        FROM message m
        JOIN member mem ON mem.id = m.member_id
        WHERE m.id = %s AND m.member_id = %s
    """, (message_id, user_id))

    result = cursor.fetchone()

    # 没有找到留言或留言不属于当前用户
    if not result:
        cursor.close()
        conn.close()
        return JSONResponse(status_code=404, content={"detail": "Message not found or access denied"})

    # 如果用户是留言的所有者，则删除留言
    cursor.execute("DELETE FROM message WHERE id = %s", (message_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return RedirectResponse(url="/member", status_code=303)


###
#使用 Uvicorn 作為服務器時，啟動時會指定端口（如果沒有指定，則使用默認端口）
    #127.0.0.1:8000 是一個特殊的 IP 地址，代表本機地址，使用 8000 這類端口能夠幫助避免與系統上運行的其他服務發生端口衝突

#main.py 是一個 Python 程式檔案，用於定義和運行 FastAPI 應用
    #cd 目標根目錄
    #uvicorn main:app --reload

#from module import item as alias
        #module：模塊名，要導入的庫或文件名。
        #item：模塊中的一個具體項目，如函數名、類名或變數名。
        #alias：為這個導入項目自定義的新名稱。
    #不一次導入所有的 FastAPI 元件，主要有以下好處:
        #明確性：單獨導入使得在查看程式碼時立即知道依賴了哪些特定的元件和功能。
        #維護性：如果專案中只用到了某些特定的功能，單獨導入可以更容易維護和理解程式碼。
        #效能：雖然從導入效能上看，差異不大，因為 Python 在導入庫時通常會載入整個模組。 但在程式碼編寫和錯誤診斷時，減少不必要的導入可以稍微提高程式碼執行效率，尤其是在解析模組時。
    #因此 from fastapi import * 雖然可以將 FastAPI 模組中所有公開的物件匯入目前命名空間。 
        #但這種方式可能會引入一些不必要的對象，如果模組跟自定義的函數或變數有命名衝突，可能會覆蓋現有的定義。
        #所以不會匯入全部

#from fastapi import FastAPI, Form, Request, Depends, HTTPException, status
    #fastapi 是一個用於構建 Web 應用的現代、快速（高性能）的 web 框架
    #從fastapi模塊導入FastAPI, Form, Request, Depends, HTTPException, status函數
        #FastAPI 類是建立所有 FastAPI 應用的核心。它用於初始化您的應用，包含路由、中間件、異常處理等的配置。
        #Form 用於從提交的表單中提取數據。它是一個依賴項，可以在函數中用作參數，來直接從表單中獲取數據。
        #Request 對象包含了請求的所有數據，比如請求頭、路徑、查詢參數等。它常在依賴注入中使用，用來訪問和處理請求數據。
        #Depends 是在 FastAPI 中實現依賴注入的函數。它用於定義一個操作的依賴項，例如用戶驗證、數據加載等，這些操作會在請求處理函數執行之前完成。
        #HTTPException 用於在處理請求時拋出 HTTP 錯誤。它允許您定義錯誤狀態碼和返回的錯誤信息。
        #status 是包含所有 HTTP 狀態碼的枚舉。這些狀態碼可以在響應或異常中使用，以表明響應的具體情況。

#from fastapi.responses import RedirectResponse, HTMLResponse
    #從fastapi模塊的子模組responses導入RedirectResponse, HTMLResponse函數
        #RedirectResponse 用於在處理完請求後重定向用戶到另一個 URL。
            #return RedirectResponse(url="/", status_code=303)
            #位置頭是 HTTP 響應頭的一部分，當發送重定向狀態碼時，它告訴瀏覽器重定向的目的地 
                #url="/"這個通常是指首頁，要自己設定指定目標網頁index.html喔，查詢@app.get("/")可以看到設定方式
            #狀態碼是服務器回應用戶請求的一種方式，告訴用戶或瀏覽器請求的狀態。
                #例如，200 表示請求成功，404 表示找不到資源，303 表示看其他位置（用於重定向）。
        #HTMLResponse 用於發送 HTML 格式的響應。
            #當需要返回 HTML 內容而不是 JSON 數據時使用。   
            #@app.get("/error", response_class=HTMLResponse)
                #這個 error 路由函數會返回一個 HTML 響應，其中包含了一個簡單的 HTML 頁面，說明發生錯誤。
                #使用 response_class=HTMLResponse 可以確保 FastAPI 正確處理並返回 HTML 內容。   

#from fastapi.staticfiles import StaticFiles
    #從fastapi模塊的子模組staticfiles導入StaticFiles函數
    #用於服務靜態文件，如 CSS、JavaScript 文件或圖片。它通常掛載在應用的特定路徑下。
        #CSS放置於static資料夾中的CSS資料夾
        #JavaScript放置於static資料夾中的js資料夾
        #圖片放置於static資料夾中的images資料夾

#Jinja2是一個強大的模板引擎，用於生成 HTML 或其他格式的文本文件，並允許在這些文件中動態地插入變量和運行簡單的邏輯
    #例如在開發一個線上商店，需要顯示不同產品的列表。可以創建一個名為 products.html 的模板，其中包含用於顯示產品的結構。
        #當一個客戶訪問商品列表頁面時：
            #應用程式會查詢數據庫以獲取所有商品的最新信息。
            #獲得的商品數據會被傳遞到 Jinja2 模板引擎。
            #模板引擎使用這些數據來填充 products.html 模板中的對應變量，例如，使用循環來為每個商品生成一個列表項。
            #完成這些步驟後，會生成一個包含所有商品信息的 HTML 頁面，這個頁面隨後會被發送到客戶的瀏覽器上顯示。
    #也就是說如果沒有Jinja2，假設有一百個商品就要建立product1.html/.../product100.html一百個網頁，而現在只需要做一個products.html

#from fastapi.templating import Jinja2Templates
    #從fastapi模塊的子模組templating導入Jinja2Templates函數
    #Jinja2Templates用於渲染 HTML 頁面。可以將數據傳遞給模板，並生成動態內容。
    #當使用 Jinja2Templates 類來整合 Jinja2 模板引擎與 FastAPI 時，通常會設置一個自定義名資料夾來存儲所有的模板文件
        #如html放置於templates資料夾

#from starlette.middleware.sessions import SessionMiddleware
    #從starlette模塊的子模組middleware.sessions導入SessionMiddleware函數
    #SessionMiddleware 用於為應用添加會話支持。它管理客戶端和服務器之間的狀態，通常用於保存用戶登入信息、購物車數據等。

#import mysql.connector
    #功能: 導入 mysql.connector 模塊，這是一個 Python 庫，用於連接到 MySQL 數據庫並執行 SQL 查詢。
    #用法: 在需要進行數據庫操作的代碼文件中導入。

#模組功能介紹完畢，接著是使用方式

##

#app = FastAPI()被賦值給變數 app
    #這樣就可以使用這個變數來訪問 FastAPI 提供的所有方法和屬性，包含路由設置、請求數據解析、響應生成等等
    #app 變數就成為了一個訪問和操作Web 應用的中心點。通過這個變數來設定和管理應用的各個方面，包括：
        #路由設置：定義不同的路由和相應的處理函數，例如使用 @app.get() 或 @app.post() 裝飾器來處理 HTTP GET 或 POST 請求
        #請求數據解析：自動解析來自客戶端的請求數據，如 URL 參數、查詢參數、JSON 請求體等，並將其提供給路由處理函數
        #響應生成：根據處理函數返回的數據，生成 HTTP 響應。這包括設置正確的 HTTP 狀態碼、生成 JSON 或 HTML 響應等
    #Web框架


#app.add_middleware(SessionMiddleware, secret_key="avl4aJqp2raF0k1o75J1ubScMbz7exGS4PdtMsYbtmY")
    #add_middleware添加中間件到app函數中，使用了SessionMiddleware管理用戶會話，並添加加密鑰匙
        #SessionMiddleware：這是一種特殊的中間件，用於在 FastAPI 應用中管理用戶會話
            #它會處理 cookie 和服務器端的會話資料，可以記住用戶是否已經登入 
        #secret_key：在 SessionMiddleware 中，secret_key 用於加密和解密會話資料，確保會話資料的安全性
            #需要使用安全的隨機字串生成器生成
    #用戶流程(用戶的登入狀態與其他資訊儲存於Cookie並以密鑰加密證明伺服器驗證過，僅有伺服器可以讀取)：
        #用戶登入
            #用戶在登入表單中輸入用戶名和密碼。
            #服務器接收到這些資料後，驗證用戶名和密碼是否正確。
            #如果驗證成功，服務器會在用戶的會話中存儲一些資料，如用戶ID和登入狀態（例如，request.session['user_id'] = user_id 和 request.session['logged_in'] = True）。
        #會話數據的保護
            #服務器使用密鑰來簽名這些會話數據，並將它們存儲在用戶瀏覽器的一個cookie中。
            #密鑰確保了會話數據的完整性，即數據在用戶的瀏覽器和服務器之間傳輸過程中沒有被修改。如果數據被修改，簽名將不匹配，服務器會拒絕接受該會話。
        #用戶發起後續請求
            #每當用戶發起後續請求（如訪問受保護的資源），瀏覽器都會自動將包含會話數據的cookie發送給服務器。
            #服務器檢查cookie中的簽名，如果簽名有效，則從會話中讀取用戶ID和登入狀態。
            #如果會話數據顯示用戶已經登入，則允許訪問受保護的資源；如果未登入或簽名不匹配，則可能重定向用戶到登入頁面。
        #用戶登出
            #當用戶選擇登出時，服務器將從會話中移除用戶ID和登入狀態，並可能清除或重設cookie。
            #此操作同樣依賴密鑰來保證任何修改都是安全的。
    #SessionMiddleware用於會話管理，CORSMiddleware用於理來自不同源的請求的安全問題，兩者功能不同在同個網站可並存
    #用戶會話管理器

#app.mount("/static", StaticFiles(directory="static"), name="static")
#mount()用於將某個目錄掛載到app變數中 FastAPI 應用的特定路徑/static
        #StaticFiles：這是一個特殊的工具，用於在 FastAPI 應用中服務靜態文件（如 HTML、CSS、JavaScript 文件、圖片等）
            #directory：這裡的 directory="static" 表示靜態文件位於項目根目錄下的 static 文件夾中    
        #name：name="static" 給這次掛載取了一個名稱，生成 URL 時可能會用到。
    #"/static" 是 URL 路徑，StaticFiles(directory="static") 創建一個處理靜態文件的應用，directory="static" 指明靜態文件存放的目錄，name="static" 是這個路徑的名稱。
        #靜態文件的掛載目錄

#templates = Jinja2Templates(directory="templates")
    #Jinja2Templates()：這個類用於整合 Jinja2 模板引擎和 FastAPI。它允許使用 Jinja2 模板語法來渲染 HTML 頁面。
    #directory：這裡的 directory="templates" 表示 Jinja2 的模板文件位於項目根目錄下的 templates 文件夾中。
    #當需要渲染一個模板時，Jinja2Templates 會在這個目錄下查找相應的 .html 文件。
    #透過這些功能的組合，可以創建一個具有用戶會話管理、靜態文件服務和 HTML 模板渲染能力的強大網路應用。
    #模板html儲存於templates資料夾


#@app.get("/")
#async def home(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request})
#當用戶訪問根目錄URL（"/"）時，觸發home函數讀取當前HTTP請求的所有數據，
#返回TemplateResponse()渲染的templates資料夾內指定的模板html，並將字典中的數據傳給指定的模板html進行渲染，而不需要每個需要的網頁都各做一個網頁
#@app.get()是一個路由裝飾器，告訴 FastAPI 當用戶訪問根 URL（"/"）時，FastAPI 應用設定了 @app.get("/") 來處理對根 URL 的 GET 請求
    #async def home 是異步函數的聲明，觸發 home 函數返回 HTML 內容，該內容隨後由瀏覽器解析並顯示給用戶。
    #templates.TemplateResponse 是一個功能，用於使用 Jinja2 模板引擎渲染 HTML 文件。這裡，它被用來生成回應的 HTML 內容。
        #"index.html" 是指定的模板文件名，這個文件應該位於 templates 文件夾中。
        #{"request": request} 是一個字典，將模板中需要的數據作為上下文傳遞給模板。
        #根 URL（"/"）指的是網站的主頁index.html
#流程說明
    #使用者進入了路由器指定/網址中
    #觸發 home 函數返回 路由器指定的HTML 內容(request: Request前者為變數，後者為路由器指定的模板HTML)
    #接著用return templates.TemplateResponse("index.html", {"request": request})去渲染這個路由器指定的HTML 內容
    #如果該網址沒有要求渲染性的東西，例如變動性的歡迎詞或者登入後指定的會員名，可以這麼寫return templates.TemplateResponse("index.html")
    #不過即使用戶未登入仍然可以獲取一些資訊，所以還是要補上哦～
        #基於用戶首選語言調整內容
        #根據用戶的地理位置顯示不同內容
        #調整基於裝置類型的顯示
        #展示首頁訪問計數
    #request: Request 代表著當前的 HTTP 請求對象。
    #這個對象封裝了所有關於當前請求的信息(客戶端與伺服器端)，包括但不限於：
        #HTTP 方法（如 GET、POST）：
          #指定了客戶端希望以何種方式與服務器資源交互（如獲取數據、提交表單等）。 
        #URL 路徑和參數：
          #URL 路徑指明了請求的資源位置。
          #路徑參數和查詢參數提供了額外的請求指定選項或信息（例如在 RESTful API 中識別資源的 ID 或者過濾結果的參數）。
        #頭部信息（Headers）：
          #包含了許多與請求相關的設定和環境信息，如內容類型、語言偏好、認證信息等。
        #用戶提交的數據（對於 POST 或 PUT 請求）：
           #例如表單數據或是在 POST 請求的主體中發送的數據。
        #Cookies：
           #由瀏覽器存儲並與請求一起發送的小段數據，常用於追蹤會話和用戶身份。
        #會話信息（如果配置了會話）：
         #如果應用使用會話追蹤（通常用於登錄狀態或用戶特定數據的持續性），這些信息可以通過 request 對象訪問。

#路由裝飾器的功能為定義
    #路徑和方法:特定的 HTTP 方法（如 GET、POST、PUT、DELETE 等）被發送到一個特定的路徑（URL）時，應該調用哪個函數
    #數據解析和響應生成:協助解析傳入的請求數據（如表單數據、JSON 負載、URL 參數等），並幫助生成響應
    #安全和驗證:與安全策略（如認證、授權）結合使用，確保只有合適的用戶可以訪問特定的路由
    #中間件和依賴注入:定義特定路由的依賴項，這意味著可以在處理請求之前先執行某些功能，如加載數據庫連接、驗證用戶身份、或者檢查請求中的數據。

#定義一個異步函數 home，這意味著它可以進行異步操作。FastAPI 會自動處理異步等待和數據返回。
    #異步函數和異步操作是現代程式設計中常見的概念，特別是在處理 I/O（輸入/輸出）操作如網路請求、檔案讀寫或數據庫查詢時。
    #這些概念尤其在 Web 開發中很重要，因為它們可以顯著提高應用效率和響應速度。
        #異步函數是指可以暫停其執行直到某些操作完成，而不阻塞其他操作或函數執行的函數。
            #異步函數的特點是它們返回一個 Awaitable 對象，這意味著可以在這個函數上使用 await 來等待它的執行完成。
            #在 FastAPI 和其他現代 Web 框架中，異步函數允許服務器在等待像數據庫查詢或檔案操作這樣的 I/O 操作完成時繼續處理其他請求
            #從而提高了應用的吞吐量和響應速度。
        #異步操作:是指在程式中發起一個可能需要等待的操作（如 I/O 操作），但不立即要求完成，並且在等待過程中，程式可以繼續執行其他任務。
            #異步操作通常用於網路請求、數據庫操作或大文件的讀寫
            #這些操作的特點是執行時間不確定，如果同步執行會導致程式阻塞，即程式需要等待操作完成後才能繼續執行下一行代碼。
        #舉個例子：
        #異步操作的實際應用例子
            #假設訪問一個需要用戶認證的網頁，並且在用戶登入後，該應用需要從一個大型數據庫中拉取用戶的個人信息和其他相關數據：
                #用戶提交登入表單：
                    #用戶在網頁上填寫自己的用戶名和密碼，然後點擊“登入”按鈕。   
                    #這個登入請求是一個 HTTP 請求，可能是一個 POST 請求，發送到服務器。
                #服務器處理登入請求：
                    #服務器接收到登入請求後，首先進行用戶身份驗證，確認用戶名和密碼是否正確。
                #異步發起數據庫查詢：
                    #一旦用戶通過身份驗證，服務器發起一個異步請求來從數據庫中拉取大量數據。這意味著服務器不需要等待數據庫請求完成就可以繼續執行其他任務。
                    #這個異步操作允許服務器處理更多的用戶請求，而不會被單一的耗時任務阻塞。
                #用戶獲得響應：
                    #即使數據還在被異步拉取，用戶已經被允許進入他的賬戶頁面。在數據庫操作完成之前，用戶可能看到一些基本的賬戶信息或者一個加載中的提示。
                #完成數據拉取：
                    #一旦數據庫操作完成，服務器將收到異步操作的結果，並可以將這些數據推送到用戶的頁面上，或者通過其他方式通知用戶數據已經準備好。

#@app.post("/signup")：
    #@app.post("/signup"): 這是一個裝飾器，用於告訴 FastAPI 該函數將處理針對 /signup 路徑(指定html)的 POST 請求。
        #POST 方法通常用於提交表單數據。
    #async def signup(request: Request, name: str = Form(...), username: str = Form(...), password: str = Form(...)): 
        #定義異步函數signup，接收 Request 對象和三個來自表單的字段：name、username 和 password(注意會對應到<input name="name/username/password">)
            #async: 表示函數是異步的，允許使用 await 進行異步操作。
            #request: Request: 表示函數接收一個包含當前 HTTP 請求所有信息的對象。
            #Form(...): 是一種依賴注入，用於從提交的表單中提取數據。
        #除request變數接收所有資訊外，又用Form(...) 明確指定從表單中提取數據)的原因是
            #雖然可以通過 request 對象手動訪問所有表單數據，但這樣做需要編寫額外的解析和驗證代碼，這增加了錯誤的可能性和開發的複雜性。
            #使用 Form(...) 簡化了這個過程，使得代碼更簡潔、更安全、更容易維護。
    #資料庫連接和操作
        #conn = mysql.connector.connect(...): 使用 MySQL Connector/Python 建立到 MySQL 數據庫的連接。
        #host="localhost": 數據庫服務器地址。
        #user="websiteuser": 用於連接數據庫的用戶名。
        #password="websitepassword": 用戶密碼。
        #database="website": 要連接的數據庫名稱。
        #cursor = conn.cursor(): 獲取一個數據庫操作的游標，用於執行 SQL 語句。
    #SQL 查詢和條件判斷
        #cursor.execute("SELECT name FROM member WHERE username = %s", (username,)): 執行 SQL 查詢，檢查是否已經存在某個用戶名。
        #member = cursor.fetchone(): 從查詢結果中獲取第一行數據（如果有的話）。如果查詢結果為空，fetchone() 返回 None。
    #用戶名存在時的處理
        #如果 member 變量不是 None（即用戶名已存在），則關閉游標和連接，並重定向到錯誤頁面。
    #用戶名不存在時的處理
        #cursor.execute("INSERT INTO member (name, username, password) VALUES (%s, %s, %s)", (name, username, password)): 如果用戶名不存在，將新用戶的信息插入到 member 表中。
        #conn.commit(): 提交事務，確保數據被保存到數據庫。
    #清理資源和結束響應
        #cursor.close(), conn.close(): 清理資源，關閉游標和連接。
        #return RedirectResponse(...): 用戶註冊成功後，重定向到首頁並顯示註冊成功的消息。






#@app.post("/signin")：
#這是一個路由裝飾器，告訴 FastAPI 當 HTTP 請求是 POST 方法並且路徑為 /signin 時，應該調用這個 signin 函數
    #HTTP POST 方法是一種常用於 Web 應用的 HTTP 請求方法。主要用於提交表單數據或上傳文件。
#async def signin(request: Request, username: str = Form(...), password: str = Form(...))：
    #async def：定義這是一個異步函數，使其能夠處理異步操作。
        #signin() 函數是一個處理用戶登入的異步函數，屬於 FastAPI 框架中的一個路由處理器。這個函數主要負責驗證用戶提交的登入資料（用戶名和密碼），並根據驗證結果重定向到相應的頁面。
        #request: Request：這是一個參數，表示當前的 HTTP 請求對象，它允許訪問請求的各種數據，如 headers 和 body。
        #username: str = Form(...) 和 password: str = Form(...)：這兩個參數用來從 POST 請求的表單數據中提取用戶名和密碼。
            #Form(...) 是一種依賴注入，用來指示 FastAPI 從提交的表單中解析這些字段。
    #條件判斷：
    #if not username or not password：檢查用戶名或密碼是否為空。
        #如果其中一個為空，則返回一個重定向響應到錯誤頁面，並帶有錯誤消息。
        #html可用<input type="text" name="username" required>
            #required屬性，如果使用者嘗試提交表單而沒有填寫這些欄位，瀏覽器會自動阻止表單提交
            #但用戶仍可能使用開發者工具移除 required 屬性，或者使用非標準瀏覽器提交表單。這樣，不完整的表單數據就可能被發送到伺服器。
            #所以雙重驗證是一個較為保守和安全的做法
    #if username == "test" and password == "test"：檢查用戶名和密碼是否都是“test”。
        #如果是，則在會話中設置 signed_in 為 True（表示用戶已登入），並重定向到會員頁面。
    #else其他狀況（帳密錯誤）則返回一個重定向響應到錯誤頁面，並帶有錯誤消息。
    #RedirectResponse(url="/error?message=請輸入用戶名和密碼", status_code=303) 和其他的 RedirectResponse：
        #RedirectResponse 是一種特殊的響應類型，用於將用戶重定向到另一個 URL。
        #url 參數指定重定向的目標 URL。
        #status_code=303：HTTP 狀態碼 303 通常用於在 POST 處理後重定向到另一個 GET 請求。


#@app.get("/member", response_class=HTMLResponse):
    #@app.get("/member"): 這是一個路由裝飾器，它告訴 FastAPI 當瀏覽器或客戶端對 /member 路徑發出 GET 請求時，應該調用下面定義的 member 函數。
        #response_class=HTMLResponse: 這個參數指定當函數返回響應時，應該使用 HTMLResponse 類來生成響應。這意味著即使不指定，返回的內容也會被處理為 HTML 格式，告訴瀏覽器這是一個 HTML 頁面。
    #async def member(request: Request):
        #async def: 這是 Python 的異步函數定義，使函數可以進行異步操作，如 I/O 操作或數據庫查詢，而不阻塞伺服器處理其他請求。
        #member: 函數名，具體執行處理 /member 請求的邏輯。
        #request: Request: 函數參數 request 是一個 Request 對象，它包含了所有關於當前 HTTP 請求的信息。在 FastAPI 中，Request 對象是從 Starlette 框架中繼承來的，提供訪問請求頭、請求體、路徑參數等數據。
    #函數內部邏輯:
        #if 'signed_in' in request.session: 
            #這條語句檢查用戶的會話中是否存在 signed_in 鍵。在 FastAPI 中，會話通常用於存儲用戶的登錄狀態或其他臨時數據。
        #return templates.TemplateResponse("member.html", {"request": request}): 
            #如果用戶已登錄（即會話中有 signed_in），
            #則返回一個由 member.html 模板渲染的 HTML 頁面。這裡 templates 是一個 Jinja2Templates 實例，用於加載和渲染指定的模板。
        #return RedirectResponse(url="/", status_code=303): 
            #如果用戶未登錄，則發送一個重定向響應，將用戶重定向到根 URL（首頁）。303 狀態碼通常用於重定向後的 GET 請求。



#@app.get("/signout"): 這是一個路由裝飾器，用於指定當用戶發出對 /signout 路徑的 GET 請求時，應調用下面定義的 signout 函數。
#async def signout(request: Request):
    #async def: 宣告這是一個異步函數，使其能夠執行非阻塞操作。
    #signout: 函數名，用於處理登出操作。
    #request: Request: 函數參數，代表當前的 HTTP 請求。Request 是一個封裝了請求相關數據（如頭部、路徑等）的對象。
#函數內部的邏輯:
    #request.session.pop('signed_in', None): 
        #這行代碼從會話中移除 signed_in 鍵。如果 signed_in 鍵不存在，則 pop 方法將默認返回 None，並且不會拋出異常。這樣做是為了清除用戶的登入狀態，準備登出用戶。
    #return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER): 
        #這行代碼創建一個重定向響應，將用戶重定向到首頁。HTTP_303_SEE_OTHER 是一個特定的 HTTP 狀態碼，用於在 POST 請求後指示客戶端進行 GET 請求。




#@app.get("/error") 表示這是一個處理 HTTP GET 請求的路由，路徑為 /error。
    #response_class=HTMLResponse 告訴 FastAPI，這個路由函數將返回 HTML 內容。
#async def error(request: Request, message: str):
    #async 表示這是一個異步函數，可以進行非阻塞的操作。
    #def error 是這個異步函數的名字。
    #request: Request 是一個參數，代表請求對象，它允許你訪問請求相關的資訊，如路徑、查詢參數等。
    #message: str 是一個從 URL 查詢參數中獲得的字符串，這個字符串會被用作顯示錯誤信息。
#return templates.TemplateResponse("error.html", {"request": request, "message": message}):
    #templates.TemplateResponse 是 Jinja2Templates 的方法，用於渲染並返回 HTML 內容。
    #"error.html" 是模板文件的名稱，這意味著這個函數將使用 templates 目錄下的 error.html 模板。
    #{"request": request, "message": message} 是一個上下文字典，傳遞給模板的變數。request 是上述的請求對象，message 是要在頁面上顯示的錯誤信息。



#當用戶訪問如 /square/3 這樣的路徑時，3 將作為 number 參數傳遞給 square 函數。
    #async def square(request: Request, number: int):
        #number: int 是從 URL 路徑中提取的參數，並指明為整數型別。
    #result = number ** 2:
        #這行代碼計算參數 number 的平方，將結果存儲在變數 result 中。
    #return templates.TemplateResponse("square_result.html", {"request": request, "number": number, "result": result}):
        #這行代碼使用模板 square_result.html 渲染結果，並將請求對象、原始數字 number 和計算結果 result 傳遞給模板。

