var followBtn = document.getElementById('followBtn');
var findGiftBtn = document.getElementById('findGiftBtn');
// 챗봇 확인용 코드 
var findGiftBtn2 = document.getElementById('findGiftBtn2');
// 챗봇 확인용 코드 


var unfollowBtn = document.getElementById('unfollowBtn');
var userId = followBtn.getAttribute('data-user-id');

// CSRF 토큰 가져오기 위한 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

followBtn.addEventListener('click', function() {
    var friendId = this.getAttribute('data-user-id'); // 팔로우할 사용자 ID 가져오기
    sendFriendRequest(friendId); // 친구 요청 함수 호출
});

function unfollowUser(userId, callback) {
    fetch(`/unfollow_user/${userId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
        })
        .then(response => response.json())
        .then(data => {
            callback(data.success); // 서버로부터의 응답에 따라 콜백을 호출합니다.
        })
        .catch(error => {
            console.error('Error:', error);
            callback(false); // 에러가 발생한 경우 실패로 간주합니다.
        });
}

// Get the modal
var modal = document.getElementById('giftModal');

// Get the button that opens the modal
var btn = document.getElementById('findGiftBtn');


// 챗봇 확인용 코드
var btn = document.getElementById('findGiftBtn2');
// 챗봇 확인용 코드

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// gpt 보내는 모달창 띄우기
btn.onclick = function() {
    modal.style.display = "block";
}

// 보내기 누르면 모달창 닫기
span.onclick = function() {
    modal.style.display = "none";
}

// 모달창 밖에 아무데나 누르면 모달창 닫기
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.getElementById('occasion').addEventListener('change', function() {
    var value = this.value;
    var birthdayPicker = document.getElementById('birthdayPicker');
    if (value === 'birthday') {
        birthdayPicker.classList.remove('hidden');
    } else {
        birthdayPicker.classList.add('hidden');
    }
});

function sendFriendRequest(friendId) {
    fetch(`/send_friend_request/${friendId}/`, { // 친구 요청 뷰로 요청 보내기
            method: "POST",
            credentials: "include",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // 요청 성공 시, 사용자에게 알림
                alert("친구 요청이 성공적으로 보내졌습니다!");
                // 필요하다면 페이지를 새로고침하거나 UI를 업데이트하여 사용자에게 상태 변경을 반영
            } else {
                // 요청 실패 시, 사용자에게 알림
                alert("친구 요청을 보낼 수 없습니다.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("친구 요청을 보낼 수 없습니다.");
        });
}