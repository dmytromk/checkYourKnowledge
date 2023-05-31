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
            //fetchTasks();
        };

       chatSocket.onclose = function(e) {
            console.error('Chat socket closed unexpectedly');
        };
          document.querySelector('#task-input-submit').onclick = function(e) {
           const ans = document.querySelector("#answear-input").value;
           const content = document.querySelector("#task-content").value;
            answer = ans;
            sendTask(ans,content);
            };

      function sendTask(ans,content) {
        console.log('sendTask');
        console.log(window.userName);
       const points = document.querySelector('#task-points').value;
       const task_name =  document.querySelector('#task-name').value;
      chatSocket.send(JSON.stringify({'command': 'new_task',
                                      'author' : username,
                                      'content' : content,
                                      'answer' : ans,
                                      'classroom_name': roomName,
                                      'points': points,
                                      'task_name': task_name}));
     showSuccessMessage();
    };
   chatSocket.onmessage = function(e) {


        };
        document.querySelector('#answear-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#answear-input-submit').click();
            }
        };
function showSuccessMessage() {
    var successDiv = document.createElement('div');
    successDiv.textContent = 'Task successfully created!';
    successDiv.className = 'success-message';

    document.body.appendChild(successDiv);

    // Remove the success message after 3 seconds
    setTimeout(function() {
        successDiv.remove();
    }, 3000);
}
