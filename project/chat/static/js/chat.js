document.addEventListener("DOMContentLoaded", function() {
    initSearchFilter();
    initMessageSending();
    initChatSelection();
    initEmojiPicker();
    initDefaultMessageDisplay();
});

//사용자가 친구를 검색할 수 있게 하는 기능을 초기화해. 입력된 검색어에 따라 친구 목록을 필터링하고 결과를 표시해.
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
        li.setAttribute("data-userid", `${person.id}`);
        li.innerHTML = `
            <img src="${person.profile_image}" alt="" onclick="goToProfile(this)" />
            <span class="name">${person.username}</span>
            <span class="name">${person.id}</span>
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

// 메시지를 보내는 기능을 초기화해. 사용자가 메시지를 입력하고 전송 버튼을 클릭하거나 
//엔터 키를 누르면 메시지가 채팅 창에 추가되도록 해.
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

            // 챗봇에 메시지 보내기
            fetch('/fetch_chatbot_message/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'message': messageText
                })
            })
            .then(response => response.json())
            .then(data => {
                const response = data.response;
                const messageItem = createMessageBubble(response, 'you');
                if (activeChat) {
                    activeChat.appendChild(messageItem);
                    activeChat.scrollTop = activeChat.scrollHeight;
                }
            })
            .catch(error => {
                console.log('Error:', error);
            });
        }
    }

    function createMessageBubble(text, className) {
        const bubble = document.createElement("div");
        bubble.className = `bubble ${className}`;
        bubble.textContent = text;
        return bubble;
    }
}

//채팅 목록에서 특정 대화를 선택할 수 있게 해주는 기능을 초기화해. 사용자가 친구 목록에서 한 명을 클릭하면 
//해당 대화가 활성화되고 나타나도록 해.
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
    if (person) {
        // 클릭된 요소가 .person 요소일 경우에만 동작
        // 모든 채팅 숨기기
        document.querySelectorAll(".chat").forEach(function(chat) {
            chat.style.display = "none";
        });
        // 선택한 사람의 채팅 보여주기
        document.querySelector(
            `.chat[data-chat="${person.dataset.chat}"]`
        ).style.display = "block";
        // 기본 메시지 숨기기
        document.getElementById("defaultMessage").style.display = "none";
    }
});

//이모지 피커 기능을 초기화해. 사용자가 이모지 버튼을 클릭하면 이모지를 선택할 수 있는 메뉴가 나타나고, 
//선택한 이모지가 메시지 입력란에 추가돼.
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
    var personElement = elem.closest(".person");
    var userID = personElement.getAttribute("data-userid");
    console.log("Redirecting to user profile with ID:", userID); // 디버깅을 위한 로그
    window.location.href = "/friend_profile/" + userID;
}

// 모든 .person 요소에 클릭 이벤트 리스너 추가
document.querySelectorAll(".person").forEach(function(person) {
    person.addEventListener("click", function() {
        // 모든 채팅 숨기기
        document.querySelectorAll(".chat").forEach(function(chat) {
            chat.style.display = "none";
        });

        // 선택한 사람의 채팅 보여주기
        var chatId = person.getAttribute("data-chat-id");
        var chatToShow = document.querySelector(`.chat[data-chat="${chatId}"]`);
        if (chatToShow) {
            chatToShow.style.display = "block";
        }

        // 기본 메시지 숨기기
        var defaultMessage = document.getElementById("defaultMessage");
        if (defaultMessage) {
            defaultMessage.style.display = "none";
        }
    });
});

function initDefaultMessageDisplay() {
    document.getElementById("defaultMessage").style.display = "flex";
}

function fetchFriendRequests() {
    fetch("/fetch_friend_requests/", { // 서버에서 친구 요청을 가져오는 URL
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.friend_requests.length > 0) {
                // 친구 요청이 있으면 알림 버튼을 표시하고, 모달에 친구 요청을 추가합니다.
                document.getElementById("friendRequestAlert").classList.remove("hidden");
                populateFriendRequestsModal(data.friend_requests);
            }
        })
        .catch((error) => console.error("Error:", error));
}

function fetchGiftRequests() {
    fetch("/fetch_gift_requests/", { // 서버에서 친구 요청을 가져오는 URL
        method: "GET",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.gift_requests.length > 0) {
            // document.getElementById("friendRequestAlert").classList.remove("hidden");
            // populateFriendRequestsModal(data.gift_requests);
            alert(data.gift_requests[0].id);
        }
    })
    .catch((error) => console.error("Error:", error));
}

function populateFriendRequestsModal(friendRequests) {
    const list = document.getElementById("friendRequestsList");
    friendRequests.forEach((request) => {
        const div = document.createElement("div");
        div.innerHTML = `
            <img style="width:100px; height:100px;" src="${request.sender_profile_image}" alt="${request.sender_name}" />
            <p>${request.sender_name} 님이 친구 요청을 보냈습니다.</p>
            <button data-request-id="${request.id}" data-action="accept">수락</button>
            <button data-request-id="${request.id}" data-action="decline">거절</button>
        `;
        list.appendChild(div);
    });
}

// 페이지 로드 시 친구 요청을 가져옵니다.
document.addEventListener("DOMContentLoaded", fetchFriendRequests);

document.getElementById("friendRequestsList").addEventListener("click", function(event) {
    const target = event.target;
    if (target.tagName === "BUTTON") {
        const requestId = target.getAttribute("data-request-id");
        const action = target.getAttribute("data-action");
        if (requestId && action) {
            manageFriendRequest(requestId, action);
        }
    }
});

document.addEventListener("DOMContentLoaded", fetchGiftRequests);

// 친구 요청을 승인하거나 거절하는 함수
function manageFriendRequest(requestId, action) {
    fetch(`/manage_friend_request/${requestId}/${action}/`, {
            method: "POST",
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"), // CSRF 토큰 필요
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert(`요청이 ${action === "accept" ? "승인되었습니다." : "거절되었습니다."}`);
                fetchFriendRequests(); // 친구 요청 데이터를 다시 가져옵니다.
                location.reload(); // 페이지 새로고침
            } else {
                alert("오류가 발생했습니다. 다시 시도해주세요.");
                location.reload(); // 오류 발생시 페이지 새로고침
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("요청 처리 중 오류가 발생했습니다.");
            location.reload(); // 오류 발생시 페이지 새로고침
        });
}


// 친구 요청 드롭다운을 표시하거나 숨기는 기능
document.getElementById("friendRequestAlert").addEventListener("mouseover", function() {
    document.getElementById("friendRequestsDropdown").classList.remove("hidden");
});

document.getElementById("friendRequestAlertContainer").addEventListener("mouseleave", function() {
    document.getElementById("friendRequestsDropdown").classList.add("hidden");
});

// CSRF 토큰 값을 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function() {
    // 예를 들어, 서버에서 전달받은 is_friend 값을 이용하여 버튼 상태 설정
    updateButtonVisibility(isFriend); // isFriend는 서버로부터 전달받은 값
});