var followBtn = document.getElementById('followBtn');
var findGiftBtn = document.getElementById('findGiftBtn');
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
    sendFriendRequest(userId, function(isFollowAccepted) {
        if (isFollowAccepted) {
            followBtn.classList.add('hidden');
            findGiftBtn.classList.remove('hidden');
            unfollowBtn.classList.remove('hidden');
        } else {
            alert('친구 요청이 거절되었습니다.');
        }
    });
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

function sendFriendRequest(receiverId, callback) {
    fetch(`/send_friend_request/${receiverId}/`, {
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