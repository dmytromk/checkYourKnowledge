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
             fetchMessages();
        };
       function fetchMessages() {
      chatSocket.send(JSON.stringify({'command': 'fetch'}));
       console.log('Hello');
    };
        chatSocket.onmessage = function(e) {
        console.log('On message');
            const data = JSON.parse(e.data);
          var message = data['message'];
          var author = data['author'];
        document.querySelector('#chat-log').value += (author + ':' + message + '\n');

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