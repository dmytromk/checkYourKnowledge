        var roomName = window.roomName;
        var username =  window.userName;

        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );
        chatSocket.onopen = function(e){
             fetchTasks();
             fetchMessages();
        };
       function fetchMessages() {
      chatSocket.send(JSON.stringify({'command': 'fetch'}));
        console.log('fetchMessages');
    };
  function fetchTasks() {
     console.log('fetchTasks');
     chatSocket.send(JSON.stringify({'command': 'fetch_task',
                                    'room_name': roomName}));
    };
        chatSocket.onmessage = function(e) {

           console.log('On message');
            const data = JSON.parse(e.data);
            console.log(data);
           if(data['type']==='chat_message'){
             const message = data['message'];
             const from = data['author'];
               const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    const chatMessages = document.getElementById('chat-messages');
    const avatarElement = document.createElement('img');
    avatarElement.classList.add('message-avatar');
    avatarElement.src = 'https://images.unsplash.com/photo-1508341591423-4347099e1f19?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8bWVufGVufDB8fDB8fHww&w=1000&q=80'; // Replace with the path to your avatar image
    messageElement.appendChild(avatarElement);

    const messageContentElement = document.createElement('div');
    messageContentElement.classList.add('message-content');

    const usernameElement = document.createElement('div');
    usernameElement.classList.add('message-username');
    usernameElement.textContent = from; // Replace with the user name
    messageContentElement.appendChild(usernameElement);

    const messageTextElement = document.createElement('div');
    messageTextElement.classList.add('message-text');
    messageTextElement.textContent = message;
    messageContentElement.appendChild(messageTextElement);

    messageElement.appendChild(messageContentElement);

    chatMessages.appendChild(messageElement);
    messageInput.value = '';

           }
           if(data['type']==='create_task'){
           var div = document.createElement('div');

           const id = data['id'];
           const message = data['message_problem'];
           const name_of_tasks = data['task_name'];
           div.className = 'customProblem';
           div.innerHTML = name_of_tasks;
           div.style.backgroundColor = '#3498db';
           div.style.padding = '10px 20px';
           div.style.color = '#fff';
           div.style.cursor = 'pointer';
           div.style.margin = '10px 0px 0px 0px';
           div.addEventListener('click', function() {

            window.location.pathname = '/chat/' + roomName + '/' + id + '/';
            });
           var parentElement = document.getElementById('content');
           parentElement.appendChild(div);
        }
        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#message-input').focus();
        document.querySelector('#message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#send-button').click();
            }
        };

        document.querySelector('#send-button').onclick = function(e) {
            const messageInputDom = document.querySelector('#message-input');
            const message = messageInputDom.value;

            chatSocket.send(JSON.stringify({
                'command' : 'new_message',
                'message': message,
                'author' : username

            }));
            messageInputDom.value = '';
        };
         document.querySelector('#createTask').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
            chatSocket.close();
            window.location.pathname = '/chat/' + roomName + '/' + 'createtask/';
        };
const header = document.getElementById('header');

const images = [
  'https://cdn.pixabay.com/photo/2014/02/27/16/10/flowers-276014_1280.jpg', // Replace with the path to your images
  'https://images.unsplash.com/photo-1610878180933-123728745d22?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2FuYWRhJTIwbmF0dXJlfGVufDB8fDB8fHww&w=1000&q=80',
  'https://natureconservancy-h.assetsadobe.com/is/image/content/dam/tnc/nature/en/photos/Zugpsitze_mountain.jpg?crop=0%2C176%2C3008%2C1654&wid=4000&hei=2200&scl=0.752'
];
