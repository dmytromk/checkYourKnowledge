const url = window.location.href;
var id = url.replace(/\/$/, "").split("/").pop();
var ans;
const chatSocket = new WebSocket(
    'ws://' +
    window.location.host +
    '/ws/chat/' +
    window.roomName +
    '/' + id
);
chatSocket.onopen = function(e) {
    console.log('Hello');
    getTask();

};

function getTask() {
    console.log('getTask');

    chatSocket.send(JSON.stringify({
        'command': 'get_task',
        'id': id,
        'classroom_name': window.roomName,
        'username': window.userName,
    }));
};
chatSocket.onmessage = function(e) {
    console.log('Some On message');
    const data = JSON.parse(e.data);
    console.log(data);

    console.log(data['type']);

    if(data['type']==='correct_answer'){
      console.log('Here');
     const points = data['points'];
      document.querySelector('#points').innerText = points + ' / ' +  points;
      var bt = document.getElementById('submitBtn');
     bt.remove();
      const p = document.createElement('p');
      p.innerText = "You have already submitted answer";
      document.querySelector('.block').appendChild(p);
    }
    else if(data['type']==='incorrect_answer'){
      console.log('Here');
     const points = data['points'];
     document.querySelector('#points').innerText = '0 / '+  points;
      var bt = document.getElementById('submitBtn');
       bt.remove();
      const p = document.createElement('p');
      p.innerText = "You have already submitted answer";
      document.querySelector('.block').appendChild(p);
    }
    else if(data['type'] === 'task_with_answer'){
    console.log('task_with_answer');
     const points = data['points'];
     
    var problem = data['message_problem'];
    ans = data['answer'];

    console.log(problem);
    document.querySelector('#problem').innerText = problem;
      var bt = document.getElementById('submitBtn');
       bt.remove();
      const p = document.createElement('p');
      p.innerText = "You have already submitted answer";
      document.querySelector('.block').appendChild(p);
      let user_ans = data['user_answer'];
       console.log(data['answer']);
       console.log(user_ans);
        if(user_ans===null){

            document.querySelector('#points').innerText = 'Maximum points: ' + points;
        }
        else if(user_ans===data['answer']){
       document.querySelector('#points').innerText = points + '/' +  points;
       }
        else if(user_ans!=data['answer']){
       document.querySelector('#points').innerText = '0 /'+  points;
       }
    }
    else{
       console.log('not task_with_answer');
     const points = data['points'];

    var problem = data['message_problem'];
    ans = data['answer'];

    console.log(problem);
    document.querySelector('#problem').innerText = problem;


      console.log(data['answer']);
        

     document.querySelector('#points').innerText = 'Maximum points: ' + points;
       
     
    }
};

function submitAnswer() {
    var answerInput = document.getElementById('answerInput');
    var resultDiv = document.getElementById('resultDiv');

    var userAnswer = answerInput.value;
     chatSocket.send(JSON.stringify({
        'command': 'save_answer',
        'id': id,
        'classroom_name': window.roomName,
        'user_ans': userAnswer,
        'username': window.userName,

    }));
    chatSocket.send(JSON.stringify({
        'command': 'check_answer',
        'id': id,
        'classroom_name': window.roomName,
        'answer_user': userAnswer,
        'username':  window.userName,

    }));


    answerInput.value = '';

}