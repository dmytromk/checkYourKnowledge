    var roomName = window.roomName;
    var username =  window.userName;
    var answear;
        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/' + 'task_1/'
            );
           chatSocket.onopen = function(e){
           var answear = window.answear;
           var content =  window.problem;

        };
          document.querySelector('#task-input-submit').onclick = function(e) {
           const ans = document.querySelector("#answear-content").value;
           const content = document.querySelector("#task-content").value;
            answear = ans;
            sendTask(ans,content);
            };
      function sendTask(ans,content) {
      chatSocket.send(JSON.stringify({'command': 'new_task',
                                      'from' : username,
                                      'content' : content,
                                      'answear' : ans}));
    };
            chatSocket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            var type = data['type']
            var author = data['from'];
            if(type == "correct_answear"){
            var answear = data['message']

             document.querySelector('#problem').value += (author + ':' + answear + '\n');
             document.querySelector('#problem').value += ('Correct\n');
            }
            if(type == "incorrect_answear"){
            var answear = data['message']
            document.querySelector('#problem').value += (author + ':' + answear + '\n');
             document.querySelector('#problem').value += ('Incorrect\n');
            }
            if(type == 'problem'){
           var message = data['message_problem'];
           document.querySelector('#problem').value += (author + ':' + message + '\n');
          }
          answear = data['message_answear'];


        };

        document.querySelector('#answear-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#answear-input-submit').click();
            }
        };

        document.querySelector('#answear-input-submit').onclick = function(e) {
            const messageInputDom = document.querySelector('#answear-input');
            const message = messageInputDom.value;
                 chatSocket.send(JSON.stringify({
                'command' : 'check_answear',
                'message': message,
                'from' : username,
                'answear': answear

            }));

            messageInputDom.value = '';
        };