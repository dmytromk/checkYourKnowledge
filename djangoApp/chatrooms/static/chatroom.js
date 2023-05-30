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
        };
       function fetchMessages() {
      chatSocket.send(JSON.stringify({'command': 'fetch'}));
       console.log('Hello');
    };
  function fetchTasks() {
     console.log('fetchTasks');
     chatSocket.send(JSON.stringify({'command': 'fetch_task',
                                    'room_name': roomName}));
    };
        chatSocket.onmessage = function(e) {
           console.log('On message');
           var div = document.createElement('div');
           const data = JSON.parse(e.data);
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

        };

        chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };

        document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#chat-message-input');
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