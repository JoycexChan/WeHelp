document.getElementById('loginForm').onsubmit = function(e) {
    var checkbox = document.querySelector('input[name="remember"]');
    if (!checkbox.checked) {
        alert('Please check the checkbox first');
        e.preventDefault(); // 防止表單提交
    }
};

function checkAndRedirect() {
    var number = document.getElementById('numberInput').value;
    number = parseInt(number); // 轉換成整數
    if (!number || number <= 0 || !Number.isInteger(number)) {
        alert('請輸入正整數');
    } else {
        window.location.href = `/square/${number}`;
    }
}










