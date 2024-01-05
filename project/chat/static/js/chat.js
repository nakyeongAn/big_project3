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

// 원본 채팅 데이터를 저장할 변수를 선언합니다.
var originalPeopleList = [];

// 페이지 로드 시 원본 채팅 목록을 저장합니다.
document.addEventListener("DOMContentLoaded", function() {
    // 다른 초기화 함수들...
    storeOriginalPeopleList();
});

// 원본 채팅 목록을 저장하는 함수
function storeOriginalPeopleList() {
    originalPeopleList = Array.from(
        document.querySelectorAll(".people .person")
    ).map(function(node) {
        return node.outerHTML; // or any other data you need
    });
}

function searchFriends() {
    var query = document.getElementById("searchInput").value;
    if (query.trim().length > 0) {
        fetch(`/search_user/?term=${encodeURIComponent(query)}`, {
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
    } else {
        // 검색창이 비었을 때 원본 채팅 목록을 표시합니다.
        updatePeopleListWithOriginal();
    }
}

// 원본 채팅 목록을 표시하는 함수
function updatePeopleListWithOriginal() {
    var peopleList = document.querySelector(".people");
    peopleList.innerHTML = ""; // 기존 목록을 비웁니다.
    originalPeopleList.forEach(function(personHTML) {
        peopleList.innerHTML += personHTML; // 원본 목록을 추가합니다.
    });
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

    // '.people' 요소에 대한 클릭 이벤트를 위임합니다.
    friends.list.addEventListener("mousedown", function(event) {
        var f = event.target.closest(".person");
        if (f && !f.classList.contains("active")) {
            setActiveChat(f, friends, chat);
        }
    });

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

// 이벤트 위임을 사용하여 .people 요소에 클릭 이벤트 리스너를 추가합니다.
document.querySelector(".people").addEventListener("click", function(event) {
    var person = event.target.closest(".person");
    if (person) { // 클릭된 요소가 .person 요소일 경우에만 동작
        // 모든 채팅 숨기기
        document.querySelectorAll(".chat").forEach(function(chat) {
            chat.style.display = "none";
        });
        // 선택한 사람의 채팅 보여주기
        document.querySelector(`.chat[data-chat="${person.dataset.chat}"]`).style.display = "block";
        // 기본 메시지 숨기기
        document.getElementById("defaultMessage").style.display = "none";
    }
});

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

// 친구 프로필 페이지 및 친구 요청 기능:
function goToProfile(elem) {
    var userID = elem.getAttribute("data-chat"); // 사용자 식별 정보
    // 페이지 이동 또는 모달 띄우기
    window.location.href = "/friend_profile?user=" + userID; // 사용자 프로필 페이지로 이동
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