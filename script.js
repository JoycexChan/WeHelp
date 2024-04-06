

function toggleStar(element) {
    console.log('Star clicked!'); // 在控制台中輸出，用於調試
    element.classList.toggle('empty');
}

function toggleMenu() {
    var popup = document.getElementById("popupMenu");
    popup.classList.toggle('show-menu'); // 切換 .show-menu 類來控制菜單的顯示和隱藏
}

function closeMenu() {
    var popup = document.getElementById("popupMenu");
    popup.classList.remove('show-menu'); // 移除 .show-menu 類來隱藏菜單
}


  function adjustViewport() {
    const width = window.innerWidth;
    let maxScale = 1; // 預設最大縮放比例

    if (width > 1200 && width <= 1920) {
      maxScale = 3;
    } else if (width > 600 && width <= 1200) {
      maxScale = 1.5; // 假設1200~1920之間最大允許放大到2倍
    } else if (width > 360 && width <= 600) {
      maxScale = 1;
    }

    document.querySelector('meta[name="viewport"]').setAttribute('content', `width=device-width, initial-scale=1, maximum-scale=${maxScale}`);
  }

  window.addEventListener('load', adjustViewport);
  window.addEventListener('resize', adjustViewport);

