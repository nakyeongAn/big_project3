document.addEventListener("DOMContentLoaded", function() {
    initSearchFilter();
    initMessageSending();
    initChatSelection();
    initEmojiPicker();
    initDefaultMessageDisplay();
});

function initSearchFilter() {
    var searchInput = document.getElementById("searchInput");
    searchInput.addEventListener("keyup", function() {
        searchFriends(searchInput.value);
    });
}

function searchFriends() {
    var query = document.getElementById("searchInput").value;
    if (query.trim().length > 0) {
        fetch(`/search-friends/?term=${encodeURIComponent(query)}`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest", // Django가 AJAX 요청으로 인식하도록 설정
                },
            })
            .then((response) => response.json())
            .then((data) => {
                updatePeopleList(data); // 검색 결과로 목록 업데이트
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    }
}

function updatePeopleList(data) {
    var peopleList = document.querySelector(".people");
    peopleList.innerHTML = ""; // 기존 목록을 비웁니다.

    data.forEach(function(person) {
        var li = document.createElement("li");
        li.className = "person";
        li.setAttribute("data-chat", `person${person.id}`);
        li.innerHTML = `
            <img src="${person.image_url}" alt="" onclick="goToProfile(this)" />
            <span class="name">${person.username}</span>
        `;
        peopleList.appendChild(li);
    });
}

function filterPeople(filterValue, peopleList) {
    var people = peopleList.getElementsByClassName("person");

    for (var i = 0; i < people.length; i++) {
        var name = people[i].getElementsByClassName("name")[0];
        if (name) {
            var nameText = name.textContent || name.innerText;
            people[i].style.display =
                nameText.toLowerCase().indexOf(filterValue) > -1 ? "" : "none";
        }
    }
}

function initMessageSending() {
    const sendButton = document.querySelector(".send");
    const messageInput = document.getElementById("message");

    sendButton.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText) {
            const newBubble = createMessageBubble(messageText, "me");
            const activeChat = document.querySelector(".chat.active-chat");
            if (activeChat) {
                activeChat.appendChild(newBubble);
                activeChat.scrollTop = activeChat.scrollHeight;
            }
            messageInput.value = "";
        }
    }

    function createMessageBubble(text, className) {
        const bubble = document.createElement("div");
        bubble.className = `bubble ${className}`;
        bubble.textContent = text;
        return bubble;
    }
}

function initChatSelection() {
    var friends = {
        list: document.querySelector("ul.people"),
        all: document.querySelectorAll(".left .person"),
        name: "",
    };
    var chat = {
        container: document.querySelector(".container .right"),
        current: null,
        person: null,
        name: document.querySelector(".container .right .top .name"),
    };

    Array.prototype.forEach.call(friends.all, function(f) {
        f.addEventListener("mousedown", function() {
            if (!f.classList.contains("active")) {
                setActiveChat(f, friends, chat);
            }
        });
    });

    function setActiveChat(f, friends, chat) {
        var active = friends.list.querySelector(".active");
        if (active) {
            active.classList.remove("active");
        }
        f.classList.add("active");
        chat.current = chat.container.querySelector(".active-chat");
        chat.person = f.getAttribute("data-chat");
        if (chat.current) {
            chat.current.classList.remove("active-chat");
        }
        var newActiveChat = chat.container.querySelector(
            '[data-chat="' + chat.person + '"]'
        );
        if (newActiveChat) {
            newActiveChat.classList.add("active-chat");
        }
        friends.name = f.querySelector(".name").innerText;
        chat.name.innerHTML = friends.name;
    }
}

function initEmojiPicker() {
    const button = document.querySelector("#emoji_btn");
    const textBox = document.querySelector("#message");
    const picker = new EmojiButton({ autoHide: false });

    button.addEventListener("click", () => {
        picker.togglePicker(button);
        requestAnimationFrame(() => {
            const pickerEl = document.querySelector(".emoji-picker");
            if (pickerEl) {
                pickerEl.style.position = "fixed";
                pickerEl.style.left = `0px`;
                pickerEl.style.top = `350px`;
            }
        });
    });

    picker.on("emoji", (emoji) => {
        textBox.value += emoji;
    });
}

// 친구목록 이미지 클릭하면  프로필 페이지 및 친구 요청 기능:
function goToProfile(elem) {
    var parentLi = elem.closest('.person');
    var userID = parentLi.getAttribute("data-chat-id"); // 사용자 식별 정보
    // 페이지 이동 또는 모달 띄우기
    window.location.href = "/friend_profile/" + userID; // 사용자 프로필 페이지로 이동
    // 또는 프로필 정보를 모달로 띄우는 등의 동작을 구현할 수 있습니다.
}

// 모든 .person 요소에 클릭 이벤트 리스너 추가
document.querySelectorAll(".person").forEach(function(person) {
    person.addEventListener("click", function() {
        // 모든 채팅 숨기기
        document.querySelectorAll(".chat").forEach(function(chat) {
            chat.style.display = "none";
        });
        // 선택한 사람의 채팅 보여주기
        document.querySelector(
            `.chat[data-chat="${this.dataset.chat}"]`
        ).style.display = "block";
        // 기본 메시지 숨기기
        document.getElementById("defaultMessage").style.display = "none";
    });
});

function initDefaultMessageDisplay() {
    document.getElementById("defaultMessage").style.display = "flex";
}