
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


