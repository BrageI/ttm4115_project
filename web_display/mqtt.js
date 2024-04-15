// Connect to MQTT broker via WebSocket
url = "wss://test.mosquitto.org:8081/mqtt"
var client = new Paho.MQTT.Client(url, "clientId-" + new Date().getTime());

// Set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// Connect the client
client.connect({onSuccess:onConnect});

// Called when the client connects
function onConnect() {
    console.log("Connected");
    // Subscribe to ttm4115/gruppe21
    client.subscribe("ttm4115/gruppe21");
}

// Called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("Connection lost:", responseObject.errorMessage);
    }
}

// Called when a message arrives
function onMessageArrived(message) {
    console.log("Message arrived:", message.payloadString);
    // Display message on the webpage
    document.getElementById("mqtt-data").innerHTML = message.payloadString;
}
