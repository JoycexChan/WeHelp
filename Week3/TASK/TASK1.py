# 功能一讀取URLs並整理成含有多個字典的list
    # 先分別存為ass1與ass2對照一下key(解析數據用的原始數據整理)
    # 找到重疊的key，以這個key為基準匯入同個list(實際程式調用的整理過的數據)
    # 可能需要正則表達式來調用分區，ImageURL只需要第一張

    # JSON格式
        # JSON（JavaScript Object Notation）是一種輕量級的資料交換格式，易於人閱讀和編寫
        # JSON主要由兩種結構組成：
            # 物件（Object）：物件在JSON中以花括號{}包裹，表示一組由鍵值對組成的無序集合(字典～)
                # {"name": "John", "age": 30, "is_student": false}
            # 陣列（Array）：陣列在JSON中以方括號[]包裹，表示一組有序的值。數組中的數值之間以逗號分隔(列表～)
                # ["apple", "banana", "cherry"]
            # JSON的資料類型
                # 字串：必須用雙引號包圍
                # 數值：可以是整數或浮點數
                # 物件：複合類型，包含一組鍵值對
                # 數組：有序的值列表
                # 布林值：true 或 false
                # null：表示空值
        # 在Python中處理JSON資料通常使用內建的json模組。(內建的模組，作業可以用～)
            # json.loads()用於將JSON格式的字串解析為Python的資料類型（如字典和列表）
                # import json
                # 載入內建的json模組

                # with open('AAA.txt', 'r', encoding='utf-8') as file:
                    # with open 它是用來打開文件並確保文件最終會被正確關閉的一種方法，無論在處理文件時是否發生異常，這稱為「上下文管理器」
                # 以open()函數來打開檔案，打開的設定包含：檔名為AAA.txt，使用'r'表示以讀取模式打開，編碼方式為utf-8
                # 並且將打開的檔案檔案存到file變數
                    # 其他模式還蠻多的，使用到再查
                    # 'w' - 寫入模式：如果檔案已存在，此模式會覆蓋原有內容；如果檔案不存在，則創建新檔案。
                    # UTF-8 是一種字符編碼，用於編碼Unicode字符。
                        # 使用UTF-8編碼的好處是能夠在不更改原有基於ASCII的系統的情況下，支持全球所有語言的字符顯示和處理
                        # 這使得UTF-8成為網頁和多語言程式設計的首選編碼方式，也是目前最普遍使用的Unicode實現方式之一       

                #     content = file.read()
                # 以read()讀取file變數，並將其儲存到名為content的變數中

                # data = json.loads(content)
                # 將讀取到的內容（現在儲存在content變數中）使用json.loads()函數解析，轉換成Python的字典或列表，並將轉換後的數據儲存到名為data的變數中
            # 而json.dumps()則用於將Python的資料類型轉換為JSON格式的字符串

    # urllib.request模塊為python標準庫，這個模塊提供了讀取URL數據的基本功能(python標準庫，作業可以用～)
        # import urllib.request
        # 載入urllib.request模塊

        # 定義URL
        # url = 'http://example.com/data'

        # urlopen()是urllib.request 模組提供的一個函數，用於打開網絡資源的 URL。這個函數可以用來訪問和獲取網頁的數據，或者是其他通過 HTTP 協議可訪問的資源
            # 當使用 urlopen() 方法時，它返回一個響應對象。這個對象提供了多種方法和屬性，用於訪問 HTTP 響應的各個部分：
                # read()：讀取響應體的內容
                # getcode()：返回 HTTP 響應的狀態碼
                # getheaders()：返回 HTTP 響應的標頭列表
                # geturl()：返回獲取資源的實際 URL，這在重定向發生時特別有用
        # 使用urllib.request模組的urlopen()打開url，並且命名為response變數
            # 當上述事情發生的時候，執行用read()來讀取response變數中的響應體內容，但通常為字節串
            # 可亦利用decode()將字節串轉換為字符串
        # with urllib.request.urlopen(url) as response:
        #     data = response.read()  
        #     text = data.decode('utf-8')

        # 道具收集完畢，把兩個模塊載入，先用urllib.request模塊處理網址，再轉成Python的字典或列表
import urllib.request # 讀取URL數據的基本功能
import json # 處理JSON資料使用內建的json模組
import re  # 導入正則表達式模塊
import csv # 載入csv模塊，可讀寫csv並支援不同分隔符與引號規則

ass1_url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1'
ass2_url = 'https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2'

with urllib.request.urlopen(ass1_url) as response_ass1_url:
    data1 = response_ass1_url.read()  
    data1_utf8 = data1.decode('utf-8')
    data1_json = json.loads(data1_utf8)

with urllib.request.urlopen(ass2_url) as response_ass2_url:
    data2 = response_ass2_url.read()  
    data2_utf8 = data2.decode('utf-8')
    data2_json = json.loads(data2_utf8)

# 錯誤 ssl.SSLCertVerificationError 發生是因為 Python 嘗試驗證 SSL 證書時未能成功。
    # 安裝證書就可以解決
    # MAC開啟終端機執行：
    # /Applications/Python\ 3.12/Install\ Certificates.command


# 取得原始資料啦data1_json跟data2_json～
# 由原始資料來看
    # A字典中的B列表的第七個C字典的D列表
        # data1_results = data1_json['A']['B'][6]['C']['D']
        # B是列表，所以訪問時需加上index索引
    # ass1_url 資料結構(字典內部的列表中的每個字典)說明：
        # 頂層字典：整個 JSON 結構包裹在一個名為 data 的字典{}中。
        # 分頁資訊：data 字典包含多個鍵值對，用於描述分頁和資料排序等信息，如 limit, offset, count, 和 sort。
        # 資料列表：results 鍵對應的值是一個列表[]，這個列表中的每個元素都是一個字典{}，包含了具體的資料項（如 "info" 等）。
    # ass2_url 資料結構(列表中的每個字典)說明：
        # 直接資料列表：JSON 結構直接以一個名為 data 的列表形式存在，不再嵌套在額外的字典中。
        # 列表元素：data 清單中的每個元素是一個字典，包含了具體的資料項，如 "MRT", "SERIAL_NO", "address" 等。
 
# ass1_url從data1_json提取data字典中的results列表，存為變數data1_results
# ass2_url從data2_json提取data列表，存為變數data2_data
data1_results = data1_json['data']['results']  
data2_data = data2_json['data']      


# 接著整理合併列表，根據功能二跟三，我們需要景點標題、地區、經度、緯度、圖片URL(第一張)、捷運站
# 資料包含非常多，但只要看我們要的東西，他們是有共同序號的，這樣就可以合併啦
    # ass1_url
        # 序號SERIAL_NO
        # 景點標題stitle
        # 經度longitude
        # 緯度latitude
        # 圖片URL(第一張)filelist，讀取第一張圖片
    # ass1_url
        # SERIAL_NO
        # 地區要從address提取，題目提示為包含區的三個中文字，正則表達式
        # 捷運站MRT


# 要以共通的SERIAL_NO來合併兩個列表，因此將其中一個列表的SERIAL_NO值轉換為字典，便於以目標SERIAL_NO快速查找
    # 舉例來說{"data":[{"MRT":"文德","SERIAL_NO":"2011051800000646","address":"臺北市  內湖區內湖路2段175號"},{"MRT":"中正紀念堂","SERIAL_NO":"2011051800000096","address":"臺北市  中正區南海路49號"}}
        # 要轉成這樣{
        # "2011051800000646": {"MRT": "文德", "SERIAL_NO": "2011051800000646", "address": "臺北市  內湖區內湖路2段175號"},
        # "2011051800000096": {"MRT": "中正紀念堂", "SERIAL_NO": "2011051800000096", "address": "臺北市  中正區南海路49號"}}
        # 搜索另一個列表中SERIAL_NO如果符合2011051800000646，就可以把同行的指定key:value匯入進去
    # 要思考以誰為主體，何者是要填入的，當填入者有多個符合，則以列表表示
        # 如何印出資料
            # for item in combined_list:
            #     print(item['A'])  # 印每個條目的A列表
            #     if item['A']:  # item['A']為真，確保列表不為空
            #         print(item['A'][0])  # 印每個條目的A列表的第一個元素
            #     else:
            #         print("沒有相關條目")
# data2_dict = {data2_item['SERIAL_NO']: data2_item for data2_item in data2_data}
    # 由後往前讀，由內往外讀，所以其實可以拆分成兩部分，後半for迴圈賦迭代值，前半data2_dict格式{key: value}
    # 建立一個字典data2_dict 格式為{key: value}
    # 通過for循環歷遍data2_data列表，每次循環時data2_item都代表列表中的一個元素
    # 如第一次迴圈為{"MRT": "文德", "SERIAL_NO": "2011051800000646", "address": "臺北市  內湖區內湖路2段175號"}）作為value
    # 接著將該次迴圈的data2_item取出SERIAL_NO的value（如第一次迴圈為2011051800000646）作為key
    # 字典格式為"2011051800000646": {"MRT": "文德", "SERIAL_NO": "2011051800000646", "address": "臺北市  內湖區內湖路2段175號"}
    # 迴圈完成其他{}
    # 存入變數data2_dict
data2_dict = {data2_item['SERIAL_NO']: data2_item for data2_item in data2_data}

# 材料準備完成開始合併數據
# 新增需要資料格式
    # 已存在
        # 序號SERIAL_NO
        # 景點標題stitle
        # 經度longitude
        # 緯度latitude
        # SERIAL_NO
        # 捷運站MRT       
    # 需新增
        # 圖片URL(第一張)filelist，讀取第一張圖片
        # 地區district要從address提取，題目提示為包含區的三個中文字，正則表達式

# 首先初始化一個combine_list列表，合併兩個列表(其中一個已轉為字典)
    # 當data1_results的['SERIAL_NO']中的值，符合data2_dict之key，則對該行進行合併數據
# 通過for循環歷遍data1_results列表，每次循環時data2_item都代表列表中的一個元素
    # 建立一個serial_no變數儲存data1_item中的SERIAL_NO的值
    # if如果serial_no變數(迭代取出的SERIAL_NO的值)in存在於data2_dict字典中，為真則執行任務
           # 注意不能反過來的原因是serial_no通常是迭代字符串，data2_dict是字典，反過來邏輯不合理  
        # 任務為將data1_item(迭代) 
            # **可以用於將調用中的字典展開，或者合併字典
                # 字典展開
                    # def print_details(name, age, job):
                    # print(f"Name: {name}, Age: {age}, Job: {job}")
                    # 如果有一個字典包含了name, age, job
                    # 例如person = {'name': 'Alice', 'age': 30, 'job': 'Engineer'}
                    # 就能用**來展開字典調用函數print_details(**person)
                # 合併字典
                    # **也能用來合併兩個或多個字典，當使用**展開兩個字典到一個新字典時，
                    # 如有重複值，後面的字典會覆蓋前面的字典，
                    # 如未重疊則新增進去
                    # 因此利用這個方式將data2_dict[serial_no]覆蓋data1_item(雖然兩者數值相同)
                    # 其目標為利用這個方式將剩餘資料新增到同一行當中，serial_no是作為定位點存在
                    # 每個迴圈完成一次就新增一行，因此將每次完成的combined_data以append()儲存延伸到combined_list的最後元素
combined_list = []

for data1_item in data1_results:
    serial_no = data1_item['SERIAL_NO']
    if serial_no in data2_dict:
        # 合并来自两个源的数据
        combined_data = {**data1_item, **data2_dict[serial_no]}
        combined_list.append(combined_data)

# 資料合併完畢，接著新增提取ImageURL資料
# 正則表達式～～～
# 迴圈 combined_list中的值用來迭代，命名為item
    # 利用get()存取item迭代值的key對應的值，並儲存為filelist變數 
        #  get('filelist', '')中的參數，第一個為指定讀取的列
        # 第二個為如果 'filelist' 鍵不存在於字典中，方法將傳回空字串。 這是一種防止程式拋出 KeyError 的常用技巧
    # urls變數＝利用re.split()切割獲取所有的URL
    # 注意將https://作為切割點會導致第0個值會是空，所以必須跳過第一個空字符串，從[1:]開始
        # re.split(pattern, string, maxsplit=0, flags=0)參數
            # pattern指定分割字串的規則，如字串將在每個 'https://' 出現的位置被分割
            # string要分割的原始字串。如包含多個連續圖片 URL 的 filelist 字串
            # maxsplit: （可選）一個整數，指定分割的最大次數。 
            # flags用於修改正規表示式的匹配方式（如大小寫敏感或不敏感）。 如果希望忽略 'https://' 大小寫，則可以使用 re.IGNORECASE
    # 如果urls存在（非空），則執行任務(else如果沒有找到URLs則設置None)
        # first_image_url變數 = 取 urls 清單的第一個元素[0]，這是第一個完整的圖片URL（不包括前綴 'https://'）
        # match變數 = 使用正則表達式來支持不同的圖片格式(jpg大小寫)
            # 使用 re.search(r'(.+?\.jpg)', first_image_url, re.IGNORECASE) 尋找符合 .jpg（不區分大小寫）的第一個符合項目
            # 這可以確保正確處理檔案名稱可能的不同大小寫形式。
                # r'(.+?\.jpg)'是指以 .jpg 結尾的字符串
                    #在Python中，前綴 r 在字串前表示該字串是一個原始字串（raw string）。因為正規表示式經常包含許多需要轉義的特殊字符，如反斜線（\）
                        # 不使用原始字符串 pattern = '\\bClass\\b'
                        # 原始字符串 pattern = r'\bClass\b'
                    # .+?盡可能少地匹配字符，直到滿足後續的模式為止
                    # \.jpg，在正規表示式中，點 . 是一個特殊字符，代表任何單個字符
                        # 要符合字面上的點，需要使用反斜線 \ 進行轉義，所以 \.jpg 實際上是在尋找文字中的 .jpg 字串
        #if match存在（非空），則執行任務
            #first_image_url =如果找到符合的圖片URL，使用 `match.group(1)` 擷取相符的部分(第一張圖片)，然後重新建構一個完整的URL
            #else 如果沒有找到匹配的圖片格式則設置None
        # 將提取的first_image_url，存入combined_list迭代的item之ImageURL。
for item in combined_list:
    filelist = item.get('filelist', '')
    urls = re.split('https://', filelist)[1:]  
    if urls:
        first_image_url = urls[0] 
        match = re.search(r'(.+?\.jpg)', first_image_url, re.IGNORECASE)
        if match:
            first_image_url = 'https://' + match.group(1)
        else:
            first_image_url = None  
    else:
        first_image_url = None  

    item['ImageURL'] = first_image_url  


# 驗證結果
# print(combined_list[0])


#接著是district資料
# 正則表達式～～～
# 注意仍在for item in combined_list:迴圈中哦，combined_list中的值用來迭代，命名為item
    # 利用get()存取item迭代值的key對應的值，並儲存為address變數 
        #  get('address', '')中的參數，第一個為指定讀取的列
        # 第二個為如果 'address' 鍵不存在於字典中，方法將傳回空字串。 這是一種防止程式拋出 KeyError 的常用技巧
    # match變數＝利用re.search()使用正規表示式尋找位址字串中符合特定模式的地區名
        # \s空白字符 \s指多個空白字符
        # \S非空白字符 \S+指多個非空白字符
        # 因此\s+(\S+區)指多個空白字符加多個連續非白字符加一個區字是搜尋目標

    #if match存在（非空），則執行任務
        #district =如果找到符合的圖片URL，使用 `match.group(1)` 擷取相符的部分
            #district = match.group(0) 回傳全部也就是包含空白字符" 中正區"
            #district = match.group(1) 回傳第一個捕獲組也就是"中正區"
            #district = match.group(2) 因為只定義了第一個捕獲組，所以問他要2會出現IndexError
        # 將提取的地區名存入 `item` 字典的新鍵 `'district'` 中。



    address = item.get('address', '') 
    match = re.search(r'\s+(\S+區)', address)  
    if match:
        district = match.group(1) 
        item['district'] = district 


# print(combined_list[0])  # 印出合併列表後的第一個元素，查看是否成功添加 ImageURL 和 district


# 功能二將每一個景點的資訊輸入到spot.csv
    # 讀取景點SpotTitle，並提取對應District,Longitude,Latitude,ImageURL輸出到到spot.csv

# 載入csv模塊，可讀寫csv並支援不同分隔符與引號規則
# 以open()函數來打開檔案，打開的設定包含：檔名為spot.csv，使用'W'表示以寫入模式打開
# newline='' 用來確保在不同操作系統中寫入時不會有額外的空行，編碼方式為utf-8，並且將打開的檔案檔案存到file變數
    # writer = csv.writer創建一個寫入器對象，用於將file資料寫入到 CSV 文件。
    # 寫入單行至 CSV 文件，首先寫入標題行['SpotTitle', 'District', 'Longitude', 'Latitude', 'ImageURL']
    # for賦予combined_list的值為迭代用item，並且執行任務
        #寫入單行至 CSV 文件（目前已有標題五列），以迴圈中迭代每個景點的資料
            # item.get('stitle', '')依序為迭代字典中取得對應的值(第一個參數)，如果不存在於字典則回傳空字符串
                # stitle對應的值,district對應的值,longitude對應的值,latitude對應的值,ImageURL對應的值




# 輸出景點資料到 spot.csv
with open('spot.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    #writer.writerow(['SpotTitle', 'District', 'Longitude', 'Latitude', 'ImageURL'])
    for item in combined_list:
        writer.writerow([item.get('stitle', ''), item.get('district', ''), item.get('longitude', ''), item.get('latitude', ''), item.get('ImageURL', '')])

# 功能三按照MRT分類輸出附近景點
    # 讀取捷運站MRT，並提取附近的景點SpotTitle，SpotTitle可以有很多個
    # 需要先構建每個捷運站對應的景點清單
# 建立mrt_spots空字典
# combined_list中的值用來迭代，命名為item
    # mrt = 從迭代值中挑選MRT列的值，如為空則回傳空字符串
    # spot_title =從迭代值中挑選stitle列的值，如為空則回傳空字符串
    # if如果迭代的mrt不存在mrt_spots字典的key中則執行任務:
        # 如果迭代的mrt不存在，初始化一個空列表，key命名迭代的mrt為來儲存景點名稱
    # 為mrt_spots中的迭代key的列表[]，添加迭代值的spot_title

mrt_spots = {}
for item in combined_list:
    mrt = item.get('MRT', '')
    spot_title = item.get('stitle', '')

    # 檢查捷運站名稱是否已經存在於 mrt_spots 中
    if mrt not in mrt_spots:
        mrt_spots[mrt] = []  # 如果不存在，初始化一個空列表來儲存景點名稱

    # 添加當前景點名稱到相應捷運站的列表中
    mrt_spots[mrt].append(spot_title)



# 載入csv模塊，可讀寫csv並支援不同分隔符與引號規則
# 以open()函數來打開檔案，打開的設定包含：檔名為mrt.csv，使用'W'表示以寫入模式打開
# newline='' 用來確保在不同操作系統中寫入時不會有額外的空行，編碼方式為utf-8，並且將打開的檔案檔案存到file變數
    # writer = csv.writer創建一個寫入器對象，用於將file資料寫入到 CSV 文件。
    # 寫入單行至 CSV 文件，首先寫入標題行['SpotTitle', 'District', 'Longitude', 'Latitude', 'ImageURL']
    # for賦予mrt_spots的key與value分別為mrt, spots迭代值，並且執行任務
            # .items()用於返回一個迭代器，它產生一系列的元組。每個元組包含兩個元素：字典的鍵（key）和相應的值（value）
        # row = [mrt] + spots
            # mrt 是一個字符串利用[]轉為列表，spots本身就是列表
            # 這是因為Python 中，只能將列表與列表相加
        # 迭代row單行寫入至 CSV 文件

with open('mrt.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for mrt, spots in mrt_spots.items():
        row = [mrt] + spots  
        writer.writerow(row)

