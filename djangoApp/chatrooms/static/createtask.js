    var roomName = window.roomName;
    var username =  window.userName;
    var answer;
        const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/' + 'createtask/'
            );
           chatSocket.onopen = function(e){
           var answear = window.answear;
           var content =  window.problem;
            fetchTasks();
        };
    function fetchTasks() {
     console.log('Hello');
     chatSocket.send(JSON.stringify({'command': 'fetch_task',
                                    'room_name': roomName}));
    };
       chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
          document.querySelector('#task-input-submit').onclick = function(e) {
           const ans = document.querySelector("#answear-content").value;
           const content = document.querySelector("#task-content").value;
            answer = ans;
            sendTask(ans,content);
            };

      function sendTask(ans,content) {

      chatSocket.send(JSON.stringify({'command': 'new_task',
                                      'author' : username,
                                      'content' : content,
                                      'answer' : ans,
                                      'classroom_name': roomName}));
    };
   chatSocket.onmessage = function(e) {
            console.log('Problem');
            const data = JSON.parse(e.data);
            console.log('Problem');
            var type = data['type']
            var author = data['author'];
            if(type == "correct_answer"){
            var answer = data['message']

             document.querySelector('#problem').value += (author + ':' + answear + '\n');
             document.querySelector('#problem').value += ('Correct\n');
            }
            if(type == "incorrect_answer"){
            var answear = data['message']
            document.querySelector('#problem').value += (author + ':' + answear + '\n');
             document.querySelector('#problem').value += ('Incorrect\n');
            }
          if(type == 'problem'){
           console.log('Problem');
           var message = data['message_problem'];
           var id = data['id'];
           document.querySelector('#problem').value += (author + ':' + message + '\n');
           var div = document.createElement('div');

           div.className = 'customProblem';
           div.innerHTML = message;
           div.style.backgroundColor = '#3498db';
           div.style.padding = '10px 20px';
           div.style.color = '#fff';
           div.style.cursor = 'pointer';

           div.addEventListener('click', function() {

            window.location.pathname = '/chat/' + roomName + '/' + id + '/';
            });
           var parentElement = document.getElementById('content');
           parentElement.appendChild(div);
          }
          answer = data['message_answer'];


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
                'command' : 'check_answer',
                'message': message,
                'from' : username,
                'answer': answer

            }));

            messageInputDom.value = '';
        };
