

function toggleStar(element) {
    console.log('Star clicked!'); // 在控制台中輸出，用於調試
    element.classList.toggle('empty');
}

document.addEventListener('DOMContentLoaded', function () {
    var stars = document.querySelectorAll('.star-icon');
    stars.forEach(function(star) {
        star.addEventListener('click', function() {
            toggleStar(this);
        });
    });
});


function toggleMenu() {
    var popup = document.getElementById("popupMenu");
    popup.classList.toggle('show-menu'); // 切換 .show-menu 類來控制菜單的顯示和隱藏
}

// 這個函數可能之前缺失了
function closeMenu() {
    var popup = document.getElementById("popupMenu");
    popup.classList.remove('show-menu'); // 移除 .show-menu 類來隱藏菜單
}
