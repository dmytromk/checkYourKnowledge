var id = url.replace(/\/$/, "").split("/").pop();
const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/' + id
        );

