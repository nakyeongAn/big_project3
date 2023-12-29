document.querySelector('.chat[data-chat=person2]').classList.add('active-chat');
document.querySelector('.person[data-chat=person2]').classList.add('active');

document.addEventListener('DOMContentLoaded', function() {
    // Get the search input field and people container
    var searchInput = document.getElementById('searchInput');
    var peopleList = document.querySelector('.people');

    // Filter people based on the search input
    function filterPeople() {
        var filterValue = searchInput.value.toLowerCase();
        var people = peopleList.getElementsByClassName('person');

        // Loop through all list items, and hide those who don't match the search query
        for (var i = 0; i < people.length; i++) {
            var name = people[i].getElementsByClassName('name')[0];
            if (name) {
                var nameText = name.textContent || name.innerText;
                if (nameText.toLowerCase().indexOf(filterValue) > -1) {
                    people[i].style.display = "";
                } else {
                    people[i].style.display = "none";
                }
            }
        }
    }

    // Attach the event listener to the search input
    searchInput.addEventListener('keyup', filterPeople);

    // Identify the send button and message input field
    const sendButton = document.querySelector('.write-link.send');
    const messageInput = document.getElementById('message');

    // Function to create a new message bubble
    function createMessageBubble(text, className) {
        const bubble = document.createElement('div');
        bubble.className = `bubble ${className}`;
        bubble.textContent = text;
        return bubble;
    }

    // Function to send a message
    function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText) {
            // Create a new message bubble as 'me' and append it to the active chat
            const newBubble = createMessageBubble(messageText, 'me');
            const activeChat = document.querySelector('.chat.active-chat');
            if (activeChat) {
                activeChat.appendChild(newBubble);
                // Scroll to the bottom of the chat
                activeChat.scrollTop = activeChat.scrollHeight;
            }

            // Clear the input field
            messageInput.value = '';
        }
    }

    // Event listener for the send button
    sendButton.addEventListener('click', sendMessage);

    // Event listener for the input field to handle "Enter" key
    messageInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default action to stop form submission
            sendMessage();
        }
    });


});


var friends = {
        list: document.querySelector('ul.people'),
        all: document.querySelectorAll('.left .person'),
        name: ''
    },
    chat = {
        container: document.querySelector('.container .right'),
        current: null,
        person: null,
        name: document.querySelector('.container .right .top .name')
    };

Array.prototype.forEach.call(friends.all, function(f) {
    f.addEventListener('mousedown', function() {
        if (!f.classList.contains('active')) {
            setActiveChat(f);
        }
    });
});

function setActiveChat(f) {
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

// <!-- emoji-picker JS-->
const button = document.querySelector("#emoji_btn");
const picker = new EmojiButton({
    // other options
    autoHide: false
});

button.addEventListener('click', (event) => {


    // Open the picker
    picker.togglePicker(button);

    // Wait for the next frame to ensure the picker is rendered
    requestAnimationFrame(() => {
        // Select the picker element, adjust the class name as necessary
        const pickerEl = document.querySelector('.emoji-picker');
        if (pickerEl) {
            // Position the picker at the click coordinates.
            pickerEl.style.position = 'fixed';
            pickerEl.style.left = `0px`;
            pickerEl.style.top = `500px`;
        }
    });
});

picker.on('emoji', emoji => {
    const textBox = document.querySelector('#message');
    textBox.value += emoji; // Append the selected emoji to the text box
});