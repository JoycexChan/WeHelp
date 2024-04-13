//TASK1

// 初始化一個對象來存儲朋友的位置信息。對象是一種包含鍵值對的數據結構
const messages = {
    "Leslie": "I'm at home near Xiaobitan station.",
    "Bob": "I'm at Ximen MRT station.",
    "Mary": "I have a drink near Jingmei MRT station.",
    "Copper": "I just saw a concert at Taipei Arena.",
    "Vivian": "I'm at Xindian station waiting for you."
};

// 初始化另一個對象來存儲每個地鐵站的線路信息
const stationInfo = {
    'Songshan': { g_line_code: 1, s_line_code: 1 },
    'Nanjing Sanmin': { g_line_code: 2, s_line_code: 2 },
    'Taipei Arena': { g_line_code: 3, s_line_code: 3 },
    'Nanjing Fuxing': {g_line_code: 4, s_line_code: 4},
    'Songgjiang Nanjing': {g_line_code: 5, s_line_code: 5},
    'Zhongshan': {g_line_code: 6, s_line_code: 6},
    'Beimen': {g_line_code: 7, s_line_code: 7},
    'Ximen': {g_line_code: 8, s_line_code: 8},
    'Xiaonanmen': {g_line_code: 9, s_line_code: 9},
    'Chiang Kai-Shek Memorial Hall': {g_line_code: 10, s_line_code: 10},
    'Guting': {g_line_code: 11, s_line_code: 11},
    'Taipower Building': {g_line_code: 12, s_line_code: 12},
    'Gongguan': { g_line_code: 13, s_line_code: 13},
    'Wanlong': { g_line_code: 14, s_line_code: 14},
    'Jingmei': { g_line_code: 15, s_line_code: 15},
    'Dapinglin': { g_line_code: 16, s_line_code: 16},
    'Qizhang': { g_line_code: 17, s_line_code: 17},
    'Xiaobitan': { g_line_code: 999, s_line_code: 18},
    'Xindian City Hall': { g_line_code: 18, s_line_code: 20},
    'Xindian': { g_line_code: 19, s_line_code: 21 }
};

// 使用 for-in 循環遍歷 messages 對象中的每個朋友
for (let friend in messages) {
    // 再次使用 for-in 循環遍歷 stationInfo 對象中的每個站點
    for (let station in stationInfo) {
        // 使用 includes 方法檢查該朋友的信息中是否包含當前站點名稱
        // includes 方法返回布爾值，判斷是否包含子字符串
        if (messages[friend].includes(station)) {
            // 如果找到站點名，則在 stationInfo 的該站點對象中添加一個新鍵 'friend_site'
            // 其值為該朋友的名字。
            stationInfo[station]['friend_site'] = friend;
        }
    }
}

// 定義一個函數 findAndPrint 用於查找並顯示與用戶輸入站點最近的朋友
function findAndPrint(messages, userInput) {
    // 使用 hasOwnProperty 方法確認 stationInfo 對象中是否存在用戶輸入的站點鍵
    // hasOwnProperty 方法用來檢查對象是否含有特定的自身屬性
    if (!stationInfo.hasOwnProperty(userInput)) {
        console.log("輸入的站名不在列表中。");
        return;
    }

    // 從 stationInfo 中獲取用戶輸入站點的 g_line_code 和 s_line_code
    const userG = stationInfo[userInput].g_line_code;
    const userS = stationInfo[userInput].s_line_code;

    let minDistance = Infinity; // 初始化最小距離為無窮大，以便比較
    let nearestFriend = null;   // 初始化最近朋友為 null
    let nearestStation = null;  // 初始化最近站點為 null

    // 再次使用 for-in 循環遍歷所有站點尋找最近的朋友
    for (let station in stationInfo) {
        // 確保該站點有 'friend_site' 屬性並且不是用戶輸入的站點
        if (stationInfo[station].hasOwnProperty('friend_site')) {
            // 計算該站點與用戶輸入站點的線路代碼差的絕對值
            const distanceG = Math.abs(userG - stationInfo[station].g_line_code);
            const distanceS = Math.abs(userS - stationInfo[station].s_line_code);
            // 選取兩者中的最小值作為距離。
            const distance = Math.min(distanceG, distanceS);

            // 如果計算的距離小於目前記錄的最小距離，更新最小距離和相關信息
            if (distance < minDistance) {
                minDistance = distance;
                nearestFriend = stationInfo[station]['friend_site'];
                nearestStation = station;
            }
        }
    }

    // 根據是否找到朋友，輸出相應信息
    if (nearestFriend) {
        console.log(nearestFriend);
    } else {
        console.log("尚未提供朋友message。");
    }
}

// 文末要記得放測試參數，函數才會運行 
findAndPrint(messages, "Wanlong"); // print Mary 
findAndPrint(messages, "Songshan"); // print Copper 
findAndPrint(messages, "Qizhang"); // print Leslie 
findAndPrint(messages, "Ximen"); // print Bob 
findAndPrint(messages, "Xindian City Hall"); // print Vivian




// TAsK2
// 初始化顧問數據：創建一個數組，其中包含顧問的對象，每個對象具有名字、評分和價格這三個屬性
    // const 通常用來宣告一個不應該改變的常量
    const consultants=[
        {"name":"John", "rate":4.5, "price":1000}, 
        {"name":"Bob", "rate":3, "price":1200}, 
        {"name":"Jenny", "rate":3.8, "price":800}
        ];
    
    // 創建一個新的數組，並為每個顧問添加一個名為 'times' 的鍵，其值為空數組
        //consultants_times變數=利用map方法，遍歷consultants數組的每個元素，對每個元素進行操作
        //consultants數組的值稱之consultant，將...consultant所有可枚舉屬性，複製到新的對象中。
        //再加上一個新的key，內容為空列表times: []
    const consultants_times = consultants.map(consultant => ({
        ...consultant,
        times: []
    }));
    
    
    
    // 定義預約函數：該函數接受顧問數組、預約的開始時間、持續時間和排序標準作為參數
        // 計算所需的時間段，使用 Array.from 來生成一個序列，這個序列從 start_time 開始，長度等於 duration時長
        // 使用 filter 和 every 組合來找出所有在 neededTimes 內都有空的顧問
            // 這個行為由內而外比較清楚
            // time => consultant.times.includes(time)檢查顧問時間是否包含特定時間點
            // 期待的是完全不符合，只要任一或者全部有符合到，都會無法預約
            // 因此利用neededTimes.some()可以找到部分符合回傳true
            // 接著利用!neededTimes.some()來反轉，回傳剩餘的顧問
                // neededTimes.every()只有當每個值都是true的時候才會返回true，做參考
            // consultants.filter()歷遍consultants所有顧問，將有空的顧問返回availableConsultants
        // 如果沒有顧問可用，直接輸出 "No Service" 並結束函數
    function book(consultants, start_time, duration, criterion) {
        const neededTimes = Array.from({ length: duration }, (_, i) => start_time + i);
    
        const availableConsultants = consultants_times.filter(consultant_time =>
            !neededTimes.some(time => consultant_time.times.includes(time))
        );
    
    
        if (availableConsultants.length === 0) {
            console.log("No Service");
            return;
        }
    
        // 使用 reduce 方法來根據用戶給定的標準找到最合適的顧問。reduce 方法遍歷顧問，並應用條件比較，保留最佳匹配
        // 設置chosenConsultant變數
        // if使用者的criterion設置為price，執行以下任務
            // chosenConsultant變數會使用availableConsultants來執行reduce(最低價格的顧問, 當前歷遍的顧問)
            // 利用三元運算符來決定是否更新累計器min
                // condition ? value1 : value2
                // 當condition為真回傳value1，當condition為假回傳value2
            // 如果當前顧問current的價格低於min中的顧問價格為真，回傳current
            // 如果當前顧問current的價格低於min中的顧問價格為假，回傳min
        // else if使用者的criterion設置為rate，執行以下任務
            // chosenConsultant變數會使用availableConsultants來執行reduce(最高評價的顧問, 當前歷遍的顧問)
            // 利用三元運算符來決定是否更新累計器max
                // condition ? value1 : value2
                // 當condition為真回傳value1，當condition為假回傳value2
            // 如果當前顧問current的評價大於max中的顧問價格為真，回傳current
            // 如果當前顧問current的評價大於max中的顧問價格為假，回傳max
        // else 剩餘的狀況就是使用者的criterion沒設置，回傳Invalid criterion
        let chosenConsultant;
        if (criterion === "price") {
            chosenConsultant = availableConsultants.reduce((min, current) =>
                current.price < min.price ? current : min
            );
        } else if (criterion === "rate") {
            chosenConsultant = availableConsultants.reduce((max, current) =>
                current.rate > max.rate ? current : max
            );
        } else {
            console.log("Invalid criterion");
            return;
        }
    
        // 從 chosenConsultant 的 times 中過濾出未被 neededTimes 包含的時間，更新其可預約時間
            // chosenConsultant原始未更新時間    
            // time => !neededTimes.includes(time) ，neededTimes包含的時間，加了驚嘆號就是neededTimes不包含的時間
            // 用neededTimes不包含的時間去篩選chosenConsultant
            // 就是還沒被預約的時間
            // 將chosenConsultant的times更新為updatedTimes
        const updatedTimes = chosenConsultant.times.filter(time =>
            !neededTimes.includes(time)
        );
        chosenConsultant.times = updatedTimes;
    
        // 更新所有顧問列表中被選中顧問的時間。這使用 forEach 循環和條件語句確保只更新對應的顧問資料
        consultants.forEach(consultant => {
            if (consultant.name === chosenConsultant.name) {
                consultant.times = chosenConsultant.times;
            }
        });
    
        // 將所需時間添加到選定顧問的 times 列表
        chosenConsultant.times.push(...neededTimes);
        // 最後輸出被選中的顧問名字
        console.log(chosenConsultant.name);
    }
        
    // 文末要記得放測試參數，函數才會運行 
    book(consultants, 15, 1, "price"); // Jenny 
    book(consultants, 11, 2, "price"); // Jenny 
    book(consultants, 10, 2, "price"); // John 
    book(consultants, 20, 2, "rate"); // John 
    book(consultants, 11, 1, "rate"); // Bob 
    book(consultants, 11, 2, "rate"); // No Service 
    book(consultants, 14, 3, "price"); // John
    
    




    
//TASK3
// 程式主體: 將使用者輸入訊息轉為程式可辨識的資料
// 定義 func 函數，使用不定數量的參數，參數通過使用 ...data 語法來接收，data 可以是任何數量的字符串(多個參數)
      // python以*對應JavaScript的...
    // let設定middleNames變數，初始化 middleNames 數組，用於存儲每個名字的中間字符
    // 使用 forEach 方法，遍歷每個名字(name在每次迭代時被賦值為 data 數組中的當前元素)，該方法適用於數組中的每個元素執行提供的函數
      // 當 data.forEach 被調用時，它將遍歷 data 數組中的每一個元素。
      // 對於每一個元素，forEach 會執行一次提供的箭頭函數=>（即回調函數）
      // 並將當前元素作為參數傳遞給這個函數。
      // name 是箭頭函數的參數，它在每次迭代時被賦值為 data 數組中的當前元素。

        // 計算每個名字的中間索引(middleIndex變數)，先用.length求名字長度，當名字長度/2時，以Ｍath.floor求其整數代表中間名的位置(觀察找出的規律)
            // Ｍath是一個內置的對象。它包含了一系列的屬性和方法，如floor讀取其中的公式 功能為提取數值的整數
            // 其他還有Math.PI 用於獲取圓周率值之類的
        // 從名字中獲取中間的字符(middleName變數)，取得當下迭代的參數(name)，獲取 name 字符串中位於 middleIndex 位置的字符。
        // 將獲得的中間字符(middleName)以push添加到 middleNames 數組的陣列末尾
function func(...data) {
    let middleNames = [];
    data.forEach(name => {
        let middleIndex = Math.floor(name.length / 2);
        let middleName = name[middleIndex];
        middleNames.push(middleName);
    });


    // 初始化 comparisonMatrix 數組，用於存儲比較矩陣   
    // 初始化 rowSums 數組，用於存儲每一行的和
    // 再次使用 forEach 方法遍歷 middleNames 來建立比較矩陣(用中間名去比較是否獨一無二)
        // 在 JavaScript 的 forEach 方法中，這個方法的回調函數可以接受三個參數：
            // 當前元素的值（element value）如middleNames中的中間名(大)
            // 當前元素的索引（index）如middleNames中的位置(0)
            // 正在操作的數組（array）(大, 明, 明)
        //無法僅僅指定 forEach 回調的第二個參數而不指定第一個!!
            // 也就是說他其實是長這樣的middleNames.forEach((element, index, arr)
            // 如果想使用索引index或整個數組array，必須在參數列表中提到元素值參數element value
            // 所以使用_作為占位符就表示：“我知道這裡有一個元素值參數，但我不需要用到它”
            // 想幫他取名也可以，所以(element, index)與(_, index)同意思
        // 外層i循環可以理解為橫行，內層j循環可以理解為縱列，形成i*j的矩陣
        // 注意這邊的i與j為索引（index），調出該位置的值來比較
            // JavaScript=== 是嚴格等值運算符，它在比較兩個值時不進行類型轉換。如果兩個值的類型不一樣，直接返回 false；只有當兩個值的類型相同且值相等時，才返回 true

            // if： i的元素與j的元素相同，在 row 中以push添加 0
            // else： if條件為假的狀況，則在 row 中以push添加 1

            // rowSum += row[row.length - 1]拆分成三部分，從最內部的部分開始看
                // 因為位置由0開始計算，因此row.length - 1 代表最後一個元素
                // row[數字] 返還row中第“數字”位置的值，記得位置由0開始計算
                // +=是一個賦值運算符，將右側表達式的值添加到左側當前變量上，加總後將新值賦予左側變量
                // 因此每次迭代時都會為row新增一個值，這行代碼就是不斷的相加，當row迭代完成時，也完成該row的加總值

    let comparisonMatrix = [];
    let rowSums = [];
    middleNames.forEach((_, i) => {
        let row = [];
        let rowSum = 0;
        middleNames.forEach((_, j) => {
            if (middleNames[i] === middleNames[j]) {
                row.push(0);
            } else {
                row.push(1);
            }
            rowSum += row[row.length - 1];
        });
        // 將完整的 row 以push添加到 comparisonMatrix 中
        // 也就是說先用內層j循環完成row，再用外層j循環完成comparisonMatrix
        comparisonMatrix.push(row);
        // 將當前行的和添加到 rowSums 中
        // 也就是說先用內層j循環完成rowSum，再用外層j循環完成rowSums
        rowSums.push(rowSum);
    });

    // 使用 indexOf 和 Math.max 方法找出 rowSums 中最大值的索引
        // ...rowSums接收多個參數
        // Math.max()求最大值
        // indexOf用來查找數組中某個元素第一次出現的位置，並返回該位置的索引，如果沒有找到元素則返回-1
        // 因此組合後為，Math.max求rowSums中最大值，並利用indexOf查詢出現的位置
        // 因為rowSums與data的參數對應的位置相同，可以利用這個方式調出符合的名字
    let maxSumIndex = rowSums.indexOf(Math.max(...rowSums));

    // if檢查 rowSums 中的最大值是否等於 data 長度減1(因為如果為獨一無二的話應該只有自己是相同，所以總數減一代表獨一無二)
    // 當if為真，利用console.log印出data中第maxSumIndex位置的值
    // else，當if為假，則輸出沒有
    if (rowSums[maxSumIndex] === data.length - 1) {
        console.log(data[maxSumIndex]);
    } else {
        console.log("沒有");
    }
}

// 文末要記得放測試參數，函數才會運行 
func("彭大牆", "陳王明雅", "吳明"); // print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // print 林花花 
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有 
func("郭宣雅", "夏曼藍波安", "郭宣恆"); // print 夏曼藍波安





//TASK4
// function定義 getNumber 函數，接收一個參數 index，表示用戶希望獲取的序列中的第幾位，
// 審題：從零開始，數值依序+4 +4 -1，循環至無限大
    // 初始化序列，第一項為 0，不要用var，依據用途改用let(可更新)或const(不可更新)
        // 關於變數的設定：python直接設定即可
        // JavaScript需要使用 let 或 const 聲明變數，如let sequence = 10來聲明變量
            // var 是最舊的變數宣告關鍵字，它提供函數作用域（function-scoped）或全域作用域
            // var（較舊的宣告關鍵字）會造成變數提升（hoisting），且 i 將有函數作用域或全域作用域，而不是區塊作用域，這可能會導致錯誤或困惑
                // 所以不要用var，改用let 
            // let let 提供區塊作用域（block-scoped），這意味著變數只能在它被宣告的區塊或子區塊中被訪問
                /* let 的例子，宣告的變數可以被更新但不能在相同作用域中被重新宣告
                    let b = 1;
                    let b = 2; 這會拋出錯誤，let 不允許在相同作用域內重新宣告
                    b = 3;  這是允許的，let 可以更新 */
            // const也提供區塊作用域，類似於 let，const 通常用來宣告一個不應該改變的常量
                /* const 的例子
                    const c = 1;
                    c = 2; 這會拋出錯誤，const 宣告的變數不能更新
                    const c = 3; 這也會拋出錯誤，const 不能重新宣告 */
    // 使用 for 循環從 1 開始，直到 index 為止，生成序列的每一項
    // i 為迭代值，從第二項開始生成（第一項為 0，第二項根據條件計算），一直到第 index + 1 項結束
        // python直接用range 函數生成一個序列，如for i in range(1, index + 1):   
        // JavaScript需要明確指定初始化，條件和增量，如for (let i = 1; i <= index; i++)：
            // 這是一個 for 迴圈，用於重複執行包含在大括號 {} 內的代碼塊。
            // 迴圈的控制變數 i 從 1 開始，每次迴圈後 i 會增加 1 (i++)，直到 i 大於 index 為止
                // let i = 1 初始化迴圈控制變數 i 為 1
                // i <= index 是迴圈繼續的條件；當 i 小於等於 index 時，迴圈繼續
                // i++ 每完成一次迴圈後，i 的值增加 1
                    // i++ 實際上是 i = i + 1 的簡寫形式。這個運算符不僅將 i 的值增加 1，還會返回 i 增加前的值
        // 判斷 i 除以 3 的餘數，根據不同的餘數進行不同的操作
        // 注意這個邏輯是根據實際序列要求去變動公式，因此要先找出序列規律
            // if 當 i 除以 3 的餘數為 1，代表每個循環的第一項要進行任務：
                // 找到sequence最後一個元素，加上4，接著這個結果進行push，將元素(計算結果)添加到現有列表的末端
                    // sequence.length 是用來獲取一個陣列 sequence 的長度
                        // 陣列的索引在 JavaScript 中（和python）是從 0 開始計數的
                        // 這意味著，如果一個陣列有 n 個元素，那麼它們的索引將會從 0 到 n-1
                        // 所以想要訪問陣列中的最後一個元素時，需要使用 陣列的長度 - 1 作為索引
                    // push() 是 JavaScript 中陣列的方法，功能與 Python 的 append() 相似，用於將一個或多個元素添加到陣列的末尾
 
                    // == 與 ===的差異
                        // Python == 用於比較兩個對象的值是否相等比較兩個相同內容的列表將返回 true
                            // Python 沒有 === 運算符。相對地，Python 使用 is 運算符來確定兩個變數是否參考至同一個對象
                        // JavaScript == 是一個等值運算符，它在比較兩個值時會進行類型轉換。如果兩個值的類型不同，JavaScript 會嘗試將它們轉換成相同類型，然後再進行比較
                            // JavaScript=== 是嚴格等值運算符，它在比較兩個值時不進行類型轉換。如果兩個值的類型不一樣，直接返回 false；只有當兩個值的類型相同且值相等時，才返回 true
                    // 代碼塊
                        //在 Python 中，冒號:用於開始一個新的代碼塊，例如在 if, for, def, class 等構造中
                            // Python 的代碼塊是根據縮排來定義的
                            // Python 通過換行來區分不同的語句
                        // 在 JavaScript 中，大括號{}用於開始一個新的代碼塊
                            // JavaScript 縮排是為了提高代碼的可讀性，不影響功能           
                            // JavaScript分號用來分隔語句，它表明一個語句的結束
                    // 條件語句 (if, elif, 和 else 結構)
                        // python: 使用 if, elif, 和 else。Python 中的 elif 是 else if 的縮寫
                        // JavaScript: 使用 if, else if, 和 else 來構建條件語句。不過，JavaScript 中的 else if 是兩個分開的關鍵字
            
                // else if當 i 除以 3 的餘數為 2，代表每個循環的第2項要進行任務：
                    // 找到sequence最後一個元素，加上4，接著這個結果進行push，將元素(計算結果)添加到現有列表的末端
                // else 不是A條件也不是B條件，剩餘的狀況為餘數=0，代表每個循環的第3項要進行任務：
                    // 找到sequence最後一個元素，加上1，接著這個結果進行push，將元素(計算結果)添加到現有列表的末端
                // 循環至使用者設定的index結束

    // 如果使用者呼叫 getNumber 函數，則輸出 sequence 序列中第 index 個數字的值
        // 注意：index 是從 0 開始排序的
        // console.log()與print() 函數有相似的功能，都用於將輸出顯示到控制台

        function getNumber(index) {
            let sequence = [0];
            for (let i = 1; i <= index; i++) {
                if (i % 3 === 1) {
                    sequence.push(sequence[sequence.length - 1] + 4);
                } else if (i % 3 === 2) {
                    sequence.push(sequence[sequence.length - 1] + 4);
                } else {
                    sequence.push(sequence[sequence.length - 1] - 1);
                }
            }
        
            console.log(sequence[index]);
        }
        
// 文末要記得放測試參數，函數才會運行 
getNumber(1); // print 4 
getNumber(5); // print 15 
getNumber(10); // print 25 
getNumber(30); // print 70