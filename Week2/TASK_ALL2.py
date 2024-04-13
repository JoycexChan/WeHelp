## TASK1

## 資料獲取: 建立字典與list

# messages 字典，不能動
messages={
"Leslie":"I'm at home near Xiaobitan station.", "Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.", "Copper":"I just saw a concert at Taipei Arena.", "Vivian":"I'm at Xindian station waiting for you."
}

# 捷運站字典載入，為每站命名代號
station_info = {
    'Songshan': {'g_line_code': 1, 's_line_code': 1},
    'Nanjing Sanmin': {'g_line_code': 2, 's_line_code': 2},
    'Taipei Arena': {'g_line_code': 3, 's_line_code': 3},
    'Nanjing Fuxing': {'g_line_code': 4, 's_line_code': 4},
    'Songgjiang Nanjing': {'g_line_code': 5, 's_line_code': 5},
    'Zhongshan': {'g_line_code': 6, 's_line_code': 6},
    'Beimen': {'g_line_code': 7, 's_line_code': 7},
    'Ximen': {'g_line_code': 8, 's_line_code': 8},
    'Xiaonanmen': {'g_line_code': 9, 's_line_code': 9},
    'Chiang Kai-Shek Memorial Hall': {'g_line_code': 10, 's_line_code': 10},
    'Guting': {'g_line_code': 11, 's_line_code': 11},
    'Taipower Building': {'g_line_code': 12, 's_line_code': 12},
    'Gongguan': {'g_line_code': 13, 's_line_code': 13},
    'Wanlong': {'g_line_code': 14, 's_line_code': 14},
    'Jingmei': {'g_line_code': 15, 's_line_code': 15},
    'Dapinglin': {'g_line_code': 16, 's_line_code': 16},
    'Qizhang': {'g_line_code': 17, 's_line_code': 17},
    'Xiaobitan': {'g_line_code': 999, 's_line_code': 18},
    'Xindian City Hall': {'g_line_code': 18, 's_line_code': 20},
    'Xindian': {'g_line_code': 19, 's_line_code': 21}
}

# 因為匯入的messages 字典的值為訊息，需要讀取訊息中的捷運站，彙整到station_info字典
# messages.items()是指遍歷 messages 字典，.items()可以將每個元素的key和value分別給friend和message變量
    # station_info.items()是指遍歷 station_info 字典
    # .items()可以將每個元素的key和value分別給station_name_with_user(僅站名)和station_data(多個值)
       # 檢查friend_message中是否包含某個捷運站名稱（station_name_with_user）
        # 如果包含，則在 station_data中添加對應的朋友名稱，Key名為 'friend_site'，值為該站的朋友名稱（friend）
 
for friend, friend_message in messages.items():
    for station_name_with_user, station_data in station_info.items():
        if station_name_with_user in friend_message:
            station_data['friend_site'] = friend



## 程式主體: 將使用者輸入訊息轉為程式可辨識的資料
## 想看目前執行是否正確時 寫入print(變數)，如print(needed_times)

# 自定義了一個名為 find_nearest_friend 的函數，接收一個參數 station_name_with_user，用來查找user_input是否包含在參數中。
    # find_nearest_friend 函數接收一個參數 station_name_with_user，這使得函數更具有一般性和重用性。
    # 函數內部不直接依賴於外部變量（比如 user_input），而是通過參數接收必要的資訊。
    # user_input 被用作 find_nearest_friend 函數的實際參數，user_input 的值在調用時傳遞給了函數的形式參數 station_name_with_user。
    # 也就是說此時station_name_with_user(本就在station_info)會加上user_input全部查詢是否在捷運站列表中，
    # 只要新增的user_input不存在於station_info，就會誘發輸入的站名不在列表中
def find_and_print(messages, user_input):
    if user_input not in station_info:
        print("輸入的站名不在列表中。")
        return

    # 從 station_info 字典中獲取輸入站名的 G 線和 S 線代碼。
    user_g = station_info[user_input]['g_line_code']
    user_s = station_info[user_input]['s_line_code']

    # 初始化尋找過程中使用的變量。
    # float('inf') 表示正無窮大。在這裡被用作 min_distance 的初始值，意味著在開始尋找之前，假定任何可能的距離都會小於這個值。
    # None 是 Python 中的一個特殊值，用來表示空或者無。
    # 將 nearest_friend 和 nearest_station 初始化為 None 表示一開始還沒有找到最近的朋友或者最近的站點。
    min_distance = float('inf')
    nearest_friend = None
    nearest_station = None

    # station_info.items()是指遍歷 station_info 字典，.items()可以將，將每個元素的key和value分別給station和data變量
        # 當data中，friend_site有內容物的時候(非none)，僅計算這些行數
            # distance_g等於求現在位點與每一個位點的差值絕對值
            # distance_s等於求現在位點與每一個位點的差值絕對值
            # 因為是求最短距離，只保留distance_g與distance_s中的最小距離
                # 對每一行的distance做迭代，直到找到最小數值
                # 如果上述為真，將 min_distance 更新為當前計算的 distance 值。(最近站點)
                # 並且將nearest_friend更替為最近站點的friend_site
                # 並且將nearest_station更替為最近站點的station
    for station, data in station_info.items():
        if 'friend_site' in data:
            distance_g = abs(user_g - data['g_line_code'])
            distance_s = abs(user_s - data['s_line_code'])
            distance = min(distance_g, distance_s)

            if distance < min_distance:
                min_distance = distance
                nearest_friend = data['friend_site']
                nearest_station = station

    # 如果nearest_friend存在表示找到最近的朋友，執行任務
        # 印出nearest_friend朋友名
        # 如果沒有找到朋友則印沒有朋友在捷運站附近，應該不會發生
    if nearest_friend:
        print(nearest_friend)
    else:
        print("尚未提供朋友message。")



## 文末要記得放測試參數，函數才會運行 
find_and_print(messages, "Wanlong") # print Mary 
find_and_print(messages, "Songshan") # print Copper 
find_and_print(messages, "Qizhang") # print Leslie 
find_and_print(messages, "Ximen") # print Bob 
find_and_print(messages, "Xindian City Hall") # print Vivian





## TASK2
## 資料獲取: 建立字典與list
# 顧問資料，未來可以維護
consultants=[
{"name":"John", "rate":4.5, "price":1000}, {"name":"Bob", "rate":3, "price":1200}, {"name":"Jenny", "rate":3.8, "price":800}
]

# 創建一個新的列表，並將consultants字典的內容加入，並且添加一個times key
# 將顧問列表複製到新列表
consultants_times = [{key: value for key, value in consultant.items()} for consultant in consultants]

# 並且為每個顧問添加一個名為 'times' 的鍵，其值為空列表
for consultant_time in consultants_times:
    consultant_time['times'] = []

#建立book函數，讀取時段start_time, 時長duration, 排序方式criterion三種使用者設定參數
def book(consultants, start_time, duration, criterion):

    # 計算需要的時段範圍，needed_times變數等於產生一個列表
    # 來源為從start_time時段開始，用range()生成的序列，
    # 當使用range時取得的值僅包含開始值，不包含結束值
        # 如時段為1，時長為2，期待結果為1, 2，故把時段與時長相加作爲結束值，即可達成目標
    needed_times = list(range(start_time, start_time + duration))

    # 根據標準過濾顧問
    # 初始化一個available_consultants列表，放置可預約的顧問
    # 從consultants_times列表中提出所有值，命名為consultant_time
        # if為真的時候，執行:後的任務
        # all() 函數接受一個可迭代對象（如列表、元组、字典等）作为参数，並返回一個布爾值
            # 如果可迭代對象中所有的元素都為真（或者沒有可迭代對象），則all() 函数返回 True
            # 如果其中任何一个元素为假，則返回 False。
            # 如此一來只要有任何一個時段不符合，該顧問就不會被添加到available_consultants列表
        # 因此if needed_times使用者期待的值全部符合的話，執行任務
        # 條件比較複雜，拆兩段
            # for time in consultant_time['times']指的是這個循環會歷遍所有的顧問字典中，times key對應的值
                # (time為局部變量，在上下文一致即可，可以改名)
                # for迴圈
            # time not in needed_times，而這個time變量不能與needed_times相符合(這表示已被預約)
        # 執行:後的任務
            # 從consultants_times列表裡的值consultant_time，提取符合的顧問，以.append添加到available_consultants

    available_consultants = []
    for  consultant_time in consultants_times:
        if all(time not in consultant_time['times'] for time in needed_times):
            available_consultants.append(consultant_time)

    if not available_consultants:
        print("No Service")
        return

    # 選擇顧問
    # 如果available_consultants列表如果為空，則印出No Service，並且return終止函數
    # 如果使用者設置的排序方式criterion符合price，則執行任務
        #chosen_consultant變量等於price排序的最小值的顧問字典
            # min()求內容物的最小值，例如print(min(1, 2, 4))  輸出: 1
            # available_consultants, key=lambda x: x['price']比較複雜
                # 調用available_consultants的值，也就是符合時段要求的顧問字典，這將是輸出的格式
                # lambda通常用於創建小的/一次性/未命名的函數，也被稱之匿名函數
                # key=lambda x: x['rate']指的是調用指定的key值
            # min(available_consultants, key=lambda x: x['price'])合併就是
            # 列出所有符合時段的顧問字典，以目標key如price比較找到最小值
            # 將有最小價格的顧問字典儲存到chosen_consultant
        # if elif else
        # if條件A為真，則執行A任務，elif如條件Ａ為假但條件B為真，則執行B任務
        # else如條件Ａ與條件B均為假，則執行C任務
        # 因此當criterion使用者設值為price時，執行任務
        # chosen_consultant變量=具有最低價格的符合時段顧問字典
        # 因此當criterion使用者設值為rating時，執行任務
        # chosen_consultant變量=具有最高評價的符合時段顧問字典
        # 不符合price以及rating的狀況則印出Invalid criterion
        # 最後return終止函數
    if not available_consultants:
        print("No Service")
        return
    if criterion == "price":
        chosen_consultant = min(available_consultants, key=lambda x: x['price'])
    elif criterion == "rate":
        chosen_consultant = max(available_consultants, key=lambda x: x['rate'])
    else:
        print("Invalid criterion")
        return



## 整理函數處理後的資料並輸出使用者目標答案：
    # 更新顧問的可用時段
    # 初始化一個updated_times空列表來儲存更新後的時間
    # 歷遍chosen_consultant字典中的times列表，每個元素賦給time變量
    # if time變量不在needed_times列表中，代表這個時間仍可以預約
    # 利用append將time加入updated_times中
    # 也就是對照後取得還可預約的時間
    updated_times = []
    for time in chosen_consultant['times']:
        if time not in needed_times:
            updated_times.append(time)
    chosen_consultant['times'] = updated_times


    # 接著同步更新到最完整consultants_times列表（全部的顧問字典）
    # consultants_times列表中的值稱之consultant_time
    # 如果consultant_time裡面的key name下的名字與hosen_consultant key name下的名字相符合，則執行任務：
    # 將consultant_time裡面的key times下的時間替換為chosen_consultant key times下的時間
    # 這樣預約後才會把該時段放進去，阻止下次預約
    for consultant_time in consultants_times:
        if consultant_time['name'] == chosen_consultant['name']:
            consultant_time['times'] = chosen_consultant['times']

    # 將所需時間添加到選定顧問的 times 列表
    # 當chosen_consultant從consultants_times中被挑選出來的時候，他其實不是新的獨立副本，而是元列表中對應字典的一個引用
    # 因此對chosen_consultant修改會同步改變consultants_times
    chosen_consultant['times'].extend(needed_times)

    print(chosen_consultant['name'])

## 文末要記得放測試參數，函數才會運行 
book(consultants, 15, 1, "price") # Jenny 
book(consultants, 11, 2, "price") # Jenny 
book(consultants, 10, 2, "price") # John 
book(consultants, 20, 2, "rate") # John 
book(consultants, 11, 1, "rate") # Bob 
book(consultants, 11, 2, "rate") # No Service 
book(consultants, 14, 3, "price") # John







## TASK3
## 程式主體: 將使用者輸入訊息轉為程式可辨識的資料
# * 符號用在函數參數前面時，表示自定義名參數data可以接收多個參數，並將它們作為一個元組（tuple）傳入函數。
# 這種參數稱為「可變位置參數」，允許你在呼叫函數時傳入任意數量的位置參數。
# 建立函數func，*data使用任意數量的位置參數
def func(*data):
    # 首先獲取每個參數的中間名
    # 初始化列表來儲存需要的參數，[]為列表 {}為字典
    # 從data讀取資料，稱之name變量
    # middle_index自定義變量代表，用len將名字個數算出來，並且用//做除法取整數，即為中間名的位置(注意從零開始)
    # middle_name為中間名，來自將data讀出的name，也就是原始全名藉由[數字]來取出目標位元中間名
    # 將指定元素middle_name添加到列表middle_names中
    middle_names = []
    for name in data:
        middle_index = len(name) // 2
        middle_name = name[middle_index]
        middle_names.append(middle_name)

    # 構建比較矩陣
    # 初始化列表comparison_matrix用來儲存比較矩陣，[]為列表 {}為字典
    # 初始化列表row_sums儲存每行的加總值，[]為列表 {}為字典

    # 從i開始到len(middle_names)參數個數結束，歷遍middle_names的資料
        # 初始化列表row用來儲存比較矩陣的一行。，[]為列表 {}為字典
    # 從j開始到len(middle_names)參數個數結束，歷遍middle_names的資料
        # i跟j的差異
            # 外層i循環可以理解為橫行
            # 內層j循環可以理解為縱列
            # i迴圈表示把每個參數(i)拿出來與其他參數(j)比較
            # 在這裏i與j的範圍一模一樣，形成i*j的矩陣

        # 注意每次迴圈只會進行一行row，再用append儲存進comparison_matrix
        # comparison_matrix儲存了很多行的row!
        # 初始化行的加總值為0。
            #比較中間字元是否相同，如果相同則添加 0 到 row 列表，否則添加 1。

        # +=是將左邊的變量與右邊元素相加，
        # row[-1]指該行中最後一個元素將最後一個元素添加到行的加總值中
        # 也就是說迭代過程中一直將數值添加上去，最終將該行完全加總
    comparison_matrix = []
    row_sums = []
    for i in range(len(middle_names)):
        row = []
        row_sum = 0  
        for j in range(len(middle_names)):
            if middle_names[i] == middle_names[j]:
                row.append(0)
            else:
                row.append(1)
            row_sum += row[-1]  
        # 迭代將row每一行添加到 comparison_matrix中
        comparison_matrix.append(row)  
        # 將行的加總值添加到 row_sums 中
        row_sums.append(row_sum)  

    # 找到加總值最大的行的索引
    max_sum_index = row_sums.index(max(row_sums))  

    # 檢查這個最大加總值是否等於 number_of_parameters -1
        # 如果獨一無二，那麼應該會與參數數量減一相當，印出每個參數的索引
        # 其他的狀況，印出沒有
    if row_sums[max_sum_index] == len(data) - 1:
        print(data[max_sum_index])
    else:
        print("沒有")   
        


## 文末要記得放測試參數，函數才會運行 
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有 
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安





## TASK4
## 程式主體: 將使用者輸入訊息轉為程式可辨識的資料
# 審題：從零開始，數值依序+4 +4 -1，循環至無限大
# 設定get_number函數，資料匯進index參數暫存，實際最終列表為sequence
    # 初始化序列，第一項為0 sequence 是一個列表（list），用來存儲生成的數列。
    # i為迭代值，從第二項開始生成(第一項為0第二項為1)，一直到第 index（使用者設定）+1 項結束
    # 這個循環決定了append()調用次數，也就是列表將被擴展多少次
        # python == 是比較運算符，用來比較兩個值是否相等。當兩邊的值相等時，表達式的結果為 True；否則為 False。
        # python 不存在 ===
    # 當i除以3的餘數為1，代表每個循環的第一項，要進行任務：
        # sequence自定義列表，進行append，將一個元素添加到現有列表的末端
        # 如果要添加固定值sequence.append(x)
        # 但因為每次添加的值都不同，因此append，將一個元素添加到現有列表的末端，獲取equence[-1]序列最後一個元素，進行計算如+ 4
    # 當i除以3的餘數為2，代表每個循環的第二項
        # 同上
    # 其餘的狀況，代表每個循環的第三項
        # 將一個元素添加到sequence列表的末端，獲取equence[-1]序列最後一個元素，進行計算如-1
    # 如果使用者呼叫get_number(index)函數，則印出sequence序列中第 index 個數字的值
    # 注意index是從0開始排序
def get_number(index):
    sequence = [0]  
    for i in range(1, index + 1):  
        if i % 3 == 1:  
          sequence.append(sequence[-1] + 4) 
        elif i % 3 == 2:  
            sequence.append(sequence[-1] + 4) 
        else:  
            sequence.append(sequence[-1] - 1) 

    print(sequence[index])

## 文末要記得放測試參數，函數才會運行 
get_number(1) # print 4
get_number(5) # print 15 
get_number(10) # print 25 
get_number(30) # print 70




