
document.getElementById('inputForm').onsubmit = function(e) {
    var checkbox = document.querySelector('input[name="remember"]');
    if (!checkbox.checked) {
        alert('Please check the checkbox first');
        e.preventDefault(); // 防止表單提交
    }
};


function confirmDelete() {
    return confirm('您確定要刪除這條留言嗎？');
}






//////

//document.getElementById('loginForm') 會獲取 ID 為 loginForm 的 HTML 元素，通常是一個 <form> 標籤。
        //.onsubmit 是一個事件處理器，它在用戶提交表單時觸發。
        //function(e) 定義了一個函數，該函數將在表單提交事件發生時被調用。e 是一個事件對象，包含了事件的相關信息。
    //var checkbox = document.querySelector('input[name="remember"]');
        //使用 querySelector 方法來選擇頁面上名稱為 remember 的 <input> 元素。
    //if (!checkbox.checked) { ... } 檢查復選框是否被勾選。如果沒有勾選，則彈出一個提示框並取消表單的提交。

//function checkAndRedirect() { ... } 定義了一個函數，用於處理當用戶點擊計算平方的按鈕時的行為。
//var number = document.getElementById('numberInput').value; 獲取用戶在 ID 為 numberInput 的輸入框中輸入的值。
//number = parseInt(number); 將獲取的值轉換成一個整數。
//if (!number || number <= 0 || !Number.isInteger(number)) { ... } 
    //這是一個條件判斷，檢查用戶輸入的是否是正整數。如果不是，彈出一個警告框提示用戶。
//else { ... } 如果檢查通過，則執行 else 語句塊內的代碼。
//window.location.href = /square/${number}; 
    //改變當前窗口的位置，導向到一個新的 URL，這裡使用模板字串來構建這個 URL，其中包含了用戶輸入的數字，這將觸發服務器計算該數字的平方。








