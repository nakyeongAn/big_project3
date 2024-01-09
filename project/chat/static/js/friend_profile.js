document.addEventListener("DOMContentLoaded", function() {
    // CSRF 토큰을 가져오는 함수
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

    // 친구 요청 보내기 함수
    function sendFriendRequest(friendId) {
        fetch(`/send_friend_request/${friendId}/`, {
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
                    alert("친구 요청이 성공적으로 보내졌습니다!");
                } else {
                    alert("친구 요청을 보낼 수 없습니다.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("친구 요청을 보낼 수 없습니다.");
            });
    }

    // 팔로우 버튼 클릭 이벤트
    var followBtn = document.getElementById('followBtn');
    if (followBtn) {
        followBtn.addEventListener('click', function() {
            var friendId = this.getAttribute('data-user-id');
            sendFriendRequest(friendId);
        });
    }

    // 프로필 사용자 설정에 대한 이벤트 위임
    document.querySelector('.profile-user-settings').addEventListener('click', function(event) {
        // 선물 알아내기 버튼 클릭
        if (event.target.id === 'findGiftBtn') {
            document.getElementById('giftModal').style.display = "block";
        }

        // 팔로우 취소 버튼 클릭
        if (event.target.id === 'unfollowBtn') {
            var userId = event.target.getAttribute('data-user-id');
            unfollowUser(userId, function(success) {
                if (success) {
                    alert("팔로우가 취소되었습니다.");
                    updateButtonVisibility(false);
                } else {
                    alert("팔로우 취소에 실패했습니다.");
                }
            });
        }
    });

    // 팔로우 취소 함수
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
                callback(data.success);
            })
            .catch(error => {
                console.error('Error:', error);
                callback(false);
            });
    }

    // 버튼 가시성 업데이트 함수
    function updateButtonVisibility(isFriend) {
        var followBtn = document.getElementById('followBtn');
        var findGiftBtn = document.getElementById('findGiftBtn');
        var unfollowBtn = document.getElementById('unfollowBtn');
        if (isFriend) {
            followBtn.classList.add('hidden');
            findGiftBtn.classList.remove('hidden');
            unfollowBtn.classList.remove('hidden');
        } else {
            followBtn.classList.remove('hidden');
            findGiftBtn.classList.add('hidden');
            unfollowBtn.classList.add('hidden');
        }
    }
    var modal = document.getElementById('giftModal');
    var span = document.getElementsByClassName("close")[0];

    // 모달창 닫기 함수
    function closeModal() {
        modal.style.display = "none";
    }

    // 보내기 버튼 또는 닫기 <span> 클릭 시 모달창 닫기
    span.onclick = function() {
        closeModal();
    }

    // 모달창 밖 클릭 시 모달창 닫기
    window.onclick = function(event) {
        if (event.target == modal) {
            closeModal();
        }
    }


});