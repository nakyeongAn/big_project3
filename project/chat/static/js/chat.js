document.addEventListener('DOMContentLoaded', function() {
    initSearchFilter();
    initMessageSending();
    initChatSelection();
    initEmojiPicker();
    initDefaultMessageDisplay();
});

function initSearchFilter() {
    var searchInput = document.getElementById('searchInput');
    var peopleList = document.querySelector('.people');

    searchInput.addEventListener('keyup', function() {
        filterPeople(searchInput.value.toLowerCase(), peopleList);
    });
}

function filterPeople(filterValue, peopleList) {
    var people = peopleList.getElementsByClassName('person');

    for (var i = 0; i < people.length; i++) {
        var name = people[i].getElementsByClassName('name')[0];
        if (name) {
            var nameText = name.textContent || name.innerText;
            people[i].style.display = nameText.toLowerCase().indexOf(filterValue) > -1 ? "" : "none";
        }
    }
}

function initMessageSending() {
    const sendButton = document.querySelector('.send');
    const messageInput = document.getElementById('message');

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText) {
            const newBubble = createMessageBubble(messageText, 'me');
            const activeChat = document.querySelector('.chat.active-chat');
            if (activeChat) {
                activeChat.appendChild(newBubble);
                activeChat.scrollTop = activeChat.scrollHeight;
            }
            messageInput.value = '';
        }
    }

    function createMessageBubble(text, className) {
        const bubble = document.createElement('div');
        bubble.className = `bubble ${className}`;
        bubble.textContent = text;
        return bubble;
    }
}

function initChatSelection() {
    var friends = {
        list: document.querySelector('ul.people'),
        all: document.querySelectorAll('.left .person'),
        name: ''
    };
    var chat = {
        container: document.querySelector('.container .right'),
        current: null,
        person: null,
        name: document.querySelector('.container .right .top .name')
    };

    Array.prototype.forEach.call(friends.all, function(f) {
        f.addEventListener('mousedown', function() {
            if (!f.classList.contains('active')) {
                setActiveChat(f, friends, chat);
            }
        });
    });

    function setActiveChat(f, friends, chat) {
        var active = friends.list.querySelector('.active');
        if (active) {
            active.classList.remove('active');
        }
        f.classList.add('active');
        chat.current = chat.container.querySelector('.active-chat');
        chat.person = f.getAttribute('data-chat');
        if (chat.current) {
            chat.current.classList.remove('active-chat');
        }
        var newActiveChat = chat.container.querySelector('[data-chat="' + chat.person + '"]');
        if (newActiveChat) {
            newActiveChat.classList.add('active-chat');
        }
        friends.name = f.querySelector('.name').innerText;
        chat.name.innerHTML = friends.name;
    }
}

function initEmojiPicker() {
    const button = document.querySelector("#emoji_btn");
    const textBox = document.querySelector('#message');
    const picker = new EmojiButton({ autoHide: false });

    button.addEventListener('click', () => {
        picker.togglePicker(button);
        requestAnimationFrame(() => {
            const pickerEl = document.querySelector('.emoji-picker');
            if (pickerEl) {
                pickerEl.style.position = 'fixed';
                pickerEl.style.left = `0px`;
                pickerEl.style.top = `350px`;
            }
        });
    });

    picker.on('emoji', emoji => {
        textBox.value += emoji;
    });
}

// 친구 프로필 페이지 및 친구 요청 기능:
function goToProfile(elem) {
    var userID = elem.getAttribute('data-chat'); // 사용자 식별 정보
    // 페이지 이동 또는 모달 띄우기
    window.location.href = '/friend_profile?user=' + userID; // 사용자 프로필 페이지로 이동
    // 또는 프로필 정보를 모달로 띄우는 등의 동작을 구현할 수 있습니다.
}

// 모든 .person 요소에 클릭 이벤트 리스너 추가
document.querySelectorAll('.person').forEach(function(person) {
    person.addEventListener('click', function() {
        // 모든 채팅 숨기기
        document.querySelectorAll('.chat').forEach(function(chat) {
            chat.style.display = 'none';
        });
        // 선택한 사람의 채팅 보여주기
        document.querySelector(`.chat[data-chat="${this.dataset.chat}"]`).style.display = 'block';
        // 기본 메시지 숨기기
        document.getElementById('defaultMessage').style.display = 'none';
    });
});

function initDefaultMessageDisplay() {
    document.getElementById('defaultMessage').style.display = 'flex';
}