
const taskName = window.taskName;
const studentName = window.studentName;

const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/' + taskName + '/'+ studentName + '/'
            );
chatSocket.onopen = function(e) {
    console.log('Hello from student tasks');
    getTask();

};
function getTask() {
    console.log('getTask');

    chatSocket.send(JSON.stringify({
        'command': 'get_task',
        'id': taskName,
        'classroom_name': window.roomName,
        'username': window.studentName,
    }));
};
chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
 if (data['type'] === 'task_with_answer') {
        console.log('task_with_answer');
        const points = data['points'];

        var problem = data['message_problem'];
        ans = data['answer'];

        console.log(problem);
        document.querySelector('#problem').innerText = problem;

        
        let user_ans = data['user_answer'];
        console.log(data['answer']);
        console.log('User_ans ' + user_ans);
        const div = document.createElement('div');
        div.innerText = user_ans;
        document.querySelector('#answers-section').appendChild(div);    
        document.querySelector('#points').innerText = data['user_points'] + '/' + data['max_points'];
    }

}
function updatePoints(newPoints) {
            var pointsElement = document.getElementById("points");
            pointsElement.innerHTML = newPoints;
                        showSuccessMessage();
        }

        document.getElementById("update-button").addEventListener("click", function() {
            var newPoints = parseInt(document.getElementById("new-points-input").value);
            if (!isNaN(newPoints)) {
                updatePoints(newPoints);
            }
        chatSocket.send(JSON.stringify({
        'command': 'change_score',
        'id': taskName,
        'classroom_name': window.roomName,
        'username': window.studentName,
        'points':  newPoints,
    }));
    });
 function showSuccessMessage() {
            var successMessage = document.getElementById("success-message");
            successMessage.style.display = "block";
            setTimeout(function() {
                successMessage.style.display = "none";
            }, 3000);
        }