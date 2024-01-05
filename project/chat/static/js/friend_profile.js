var followBtn = document.getElementById('followBtn');
var findGiftBtn = document.getElementById('findGiftBtn');
var unfollowBtn = document.getElementById('unfollowBtn');


document.getElementById('followBtn').addEventListener('click', function() {
    // Simulate the other user accepting the follow request
    // In a real application, you would check this with a server
    let isFollowAccepted = true; // This should be dynamic based on actual user interaction

    if (isFollowAccepted) {
        // Hide the 'Follow' button
        this.classList.add('hidden');

        // Show the 'Find Gift' and 'Unfollow' buttons
        document.getElementById('findGiftBtn').classList.remove('hidden');
        document.getElementById('unfollowBtn').classList.remove('hidden');
    }
});

document.getElementById('unfollowBtn').addEventListener('click', function() {
    // Simulate unfollowing the user successfully
    // In a real application, you would check this with a server
    let isUnfollowSuccessful = true; // This should be dynamic based on actual user interaction

    if (isUnfollowSuccessful) {
        // Show the 'Follow' button
        document.getElementById('followBtn').classList.remove('hidden');

        // Hide the 'Find Gift' and 'Unfollow' buttons
        document.getElementById('findGiftBtn').classList.add('hidden');
        this.classList.add('hidden'); // 'this' refers to 'unfollowBtn'
    }
});

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

function sendFriendRequest() {
    // 서버에 친구 요청을 보내는 AJAX 요청 구현
}