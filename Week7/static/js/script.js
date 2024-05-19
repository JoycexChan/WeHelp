document.getElementById('inputForm').onsubmit = function(e) {
    const checkbox = document.querySelector('input[name="remember"]');
    if (!checkbox.checked) {
        alert('Please check the checkbox first');
        e.preventDefault(); // 防止表單提交
    }
};


function confirmDelete() {
    return confirm('您確定要刪除這條留言嗎？');
}

async function fetchMemberData() {
    const username = document.getElementById('usernameInput').value;
    if (!username.trim()) {
        document.getElementById('memberInfo').textContent = '请输入用户名。';
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/member?username=${encodeURIComponent(username)}`, {
            method: 'GET',
            credentials: 'include' // 確保攜帶 cookies，支持跨域請求
        });

        if (!response.ok) {
            throw new Error('Failed to fetch data: ' + response.statusText);
        }

        const result = await response.json();

        const memberInfo = document.getElementById('memberInfo');
        if (result.data && result.data.name) {
            // 確認 data 不是 null 並寫包含用戶信息
            memberInfo.textContent = `${result.data.name} (${result.data.username})`;
        } else if (result.data === null) {
            // 處理沒有找到數據或者未登錄的狀況
            memberInfo.textContent = 'No Data or not logged in';
        }
    } catch (error) {
        console.error('Fetch error:', error);
        document.getElementById('memberInfo').textContent = '加載數據失敗。';
    }
}


async function updateMemberName() {
    const newName = document.getElementById('newNameInput').value;  // 從輸入欄位獲取新名字
    if (!newName.trim()) {
        document.getElementById('updateStatus').textContent = '名字不能為空。';
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/member', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: newName })  // 發送JSON格式的請求體
        });

        const data = await response.json();  // 解析JSON響應

        // 根據後端響應更新狀態文字
        if (response.ok && data.ok) {
            document.getElementById('updateStatus').textContent = '更新成功！';
        } else {
            document.getElementById('updateStatus').textContent = '更新失敗。';
        }
    } catch (error) {  // 捕獲異常
        console.error('更新失敗:', error);
        document.getElementById('updateStatus').textContent = '更新失敗：網絡或服務器錯誤';
    }
}

