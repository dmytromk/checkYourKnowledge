var roomName = window.roomName;
var username = window.userName;
const messageInput = document.querySelector('#messageInput');
const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    roomName +
    '/'
);
chatSocket.onopen = function(e) {
    fetchTasks();
    fetchMessages();
};

function fetchMessages() {

    chatSocket.send(JSON.stringify({
        'command': 'fetch',
        'room_name': roomName
    }));
    console.log('fetchMessages');
};

function fetchTasks() {
    console.log('fetchTasks');
    chatSocket.send(JSON.stringify({
        'command': 'fetch_task',
        'room_name': roomName
    }));


};
chatSocket.onmessage = function(e) {

    console.log('On message');
    const data = JSON.parse(e.data);
    console.log(data);
    console.log(data['command']);
    if(data['command']==='messages'){
        console.log('messages');
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML="";
        for (let i=0; i<data['messages'].length; i++) {
            console.log(data['messages'][i]);
            createMessage(data['messages'][i]);
        }

    }
    if(data['command']==='tasks'){
        console.log('messages');
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML="";
        for (let i=0; i<data['tasks'].length; i++) {
            console.log(data['tasks'][i]);
            createTask(data['tasks'][i]);
        }

    }
    else if (data['type'] === 'chat_message') {

        createMessage(data);
        messageInput.value = '';


    }
    else if (data['type'] === 'create_task') {
        createTask(data);
    }
};
function createTask(data) {
    const TaskName = data['task_name'];
    const pointsInt = data['points'];
    const id = data['id'];

    var div = document.createElement('div');
    div.style.backgroundColor = '#3498db';
    div.style.padding = '10px';
    div.style.color = '#fff';
    div.style.cursor = 'pointer';
    div.style.margin = '10px 0';



    // Create the task name element
    var taskName = document.createElement('h3');
    taskName.style.fontWeight = 'bold';
    taskName.style.marginBottom = '5px';
    taskName.textContent = TaskName;
    div.appendChild(taskName);

    // Create the points element
    var points = document.createElement('p');
    points.style.margin = '0';
    points.textContent = 'Points: ' + String(pointsInt); // Replace '10' with the actual points value
    div.appendChild(points);

    // Add the click event listener
    div.addEventListener('click', function() {
        window.location.pathname = '/chat/' + roomName + '/' + id + '/';
    });

    // Append the div to the parent element
    var parentElement = document.getElementById('content');
    parentElement.appendChild(div);
}

function createMessage(data) {
    const message = data['content'];
    const from = data['author'];
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    const chatMessages = document.getElementById('chat-messages');

    const avatarElement = document.createElement('img');
    avatarElement.classList.add('message-avatar');
    avatarElement.src = 'https://images.unsplash.com/photo-1508341591423-4347099e1f19?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8bWVufGVufDB8fDB8fHww&w=1000&q=80';
    messageElement.appendChild(avatarElement);

    const messageContentElement = document.createElement('div');
    messageContentElement.classList.add('message-content');

    const usernameElement = document.createElement('div');
    usernameElement.classList.add('message-username');
    if (from === username) {
        usernameElement.textContent = 'You';
    } else {
        usernameElement.textContent = from;
    }
    messageContentElement.appendChild(usernameElement);

    const messageTextElement = document.createElement('div');
    messageTextElement.classList.add('message-text');
    messageTextElement.textContent = message;
    messageContentElement.appendChild(messageTextElement);

    messageElement.appendChild(messageContentElement);

    chatMessages.appendChild(messageElement);
}
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#message-input').focus();
document.querySelector('#message-input').onkeyup = function(e) {
    if (e.keyCode === 13) { // enter, return
        document.querySelector('#send-button').click();
    }
};


document.querySelector('#send-button').onclick = function(e) {
    const messageInputDom = document.querySelector('#message-input');
    const message = messageInputDom.value;

    chatSocket.send(JSON.stringify({
        'command': 'new_message',
        'message': message,
        'author': username,
        'classroom_name': roomName

    }));
    messageInputDom.value = '';
};
document.querySelector('#createTask').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    chatSocket.close();
    window.location.pathname = '/chat/' + roomName + '/' + 'createtask/';
};

document.querySelector('#generate-link').onclick = function(e) {
    chatSocket.send(JSON.stringify({
        'command' : 'generate_invite',
        'token': roomName
    }));
};

const header = document.getElementById('header');
