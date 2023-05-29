const url = window.location.href;
var id = url.replace(/\/$/, "").split("/").pop();
var ans;
const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            +  window.roomName
            + '/' + id
        );
    chatSocket.onopen = function(e){
            console.log('Hello');
            getTask();

    };
     function getTask() {
      console.log('Hello');
     chatSocket.send(JSON.stringify({'command': 'get_task',
                                     'id': id,
                                      'classroom_name': window.roomName}));
    };
     chatSocket.onmessage = function(e) {
        console.log('On message');
         const data = JSON.parse(e.data);
         console.log(data);
         var problem = data['message_problem'];
        ans = data['answer']
         console.log(problem);
         document.querySelector('#problem').innerText = problem;

        };
       function submitAnswer() {
      var answerInput = document.getElementById('answerInput');
      var resultDiv = document.getElementById('resultDiv');

      var userAnswer = answerInput.value;

      if (userAnswer === ans) {
        resultDiv.textContent = 'Correct answer!';
        resultDiv.style.color = 'green';
      } else {
        resultDiv.textContent = 'Incorrect answer. Please try again.';
        resultDiv.style.color = 'red';
      }

      answerInput.value = '';
    }