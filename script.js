
function toggleMenu() {
    let popup = document.getElementById("popupMenu");
    popup.classList.toggle('show-menu'); // 切換 .show-menu 類來控制菜單的顯示和隱藏
}

function closeMenu() {
    let popup = document.getElementById("popupMenu");
    popup.classList.remove('show-menu'); // 移除 .show-menu 類來隱藏菜單
}

function toggleStar(element) {
    console.log('Star clicked!'); // 在控制台中輸出，用於調試
    element.classList.toggle('empty');
}

document.addEventListener('DOMContentLoaded', function () {
    let stars = document.querySelectorAll('.star-icon');
    stars.forEach(function(star) {
        star.addEventListener('click', function() {
            toggleStar(this);
        });
    });
});




function updateBoxes(selector, spots) {
    const boxes = document.querySelectorAll(selector);
    spots.forEach((spot, index) => {
        if (index >= boxes.length) return;
    
        const filelist = spot.filelist ? spot.filelist.split(/http:\/\/|https:\/\//).filter(url => url.match(/\.(jpg|JPG)$/)) : [];
        const firstImage = filelist.length > 0 ? 'https://' + filelist[0] : 'default-image.jpg';
    
        const box = boxes[index];

        if (selector === '.A-box') {
            let imgElement = box.querySelector('img');
            if (!imgElement) {
                imgElement = document.createElement('img');
                box.appendChild(imgElement);
            }
            imgElement.src = firstImage;
            imgElement.alt = spot.stitle;
        } else if (selector === '.B-box') {
            let imgDiv = box.querySelector('.B1-img-box');
            if (!imgDiv) {
                imgDiv = document.createElement('div');
                imgDiv.className = 'B1-img-box';
                box.appendChild(imgDiv);
            }
            imgDiv.style.backgroundImage = `url('${firstImage}')`;
        }
    
        let textBox = box.querySelector(selector === '.A-box' ? '.A1-text-box' : '.B1-text-box');
        if (!textBox) {
            textBox = document.createElement('div');
            textBox.className = selector === '.A-box' ? 'A1-text-box' : 'B1-text-box';
            box.appendChild(textBox);
        }
        textBox.textContent = spot.stitle;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    fetch('https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1')
    .then(response => response.json())
    .then(data => {
        const results = data.data.results;
        updateBoxes('.A-box', results.slice(0, 3)); // 使用3筆數據更新3個A-box
        updateBoxes('.B-box', results.slice(3, 13)); // 使用第3～13筆數據更新10個B-box
    })
    .catch(error => console.error('Error fetching data:', error));
});
