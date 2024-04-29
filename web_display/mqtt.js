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
    client.subscribe("ttm4115/gruppe21/fromserver");
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
    var data = JSON.parse(message.payloadString);
    if (data["location_id"] === 0) {
        document.getElementById("mqtt-location-0").innerHTML = data["location_name"]
        document.getElementById("mqtt-available-0").innerHTML = "Available chargers: " + data["available_chargers"]
        document.getElementById("mqtt-available-arrival-0").innerHTML = "Estimated available chargers on arrival: " + data["available_chargers_arrival"]
        document.getElementById("mqtt-total-0").innerHTML = "Total amount of chargers: " + data["total_chargers"]
        document.getElementById("mqtt-time-0").innerHTML = "Time until arrival: " + data ["time_until_arrival"]
    }
    if (data["location_id"] === 1) {
        document.getElementById("mqtt-location-1").innerHTML = data["location_name"]
        document.getElementById("mqtt-available-1").innerHTML = "Available chargers: " + data["available_chargers"]
        document.getElementById("mqtt-available-arrival-1").innerHTML = "Estimated available chargers on arrival: " + data["available_chargers_arrival"]
        document.getElementById("mqtt-total-1").innerHTML = "Total amount of chargers: " + data["total_chargers"]
        document.getElementById("mqtt-time-1").innerHTML = "Time until arrival: " + data ["time_until_arrival"]
    }
    if (data["location_id"] === 2) {
        document.getElementById("mqtt-location-2").innerHTML = data["location_name"]
        document.getElementById("mqtt-available-2").innerHTML = "Available chargers: " + data["available_chargers"]
        document.getElementById("mqtt-available-arrival-2").innerHTML = "Estimated available chargers on arrival: " + data["available_chargers_arrival"]
        document.getElementById("mqtt-total-2").innerHTML = "Total amount of chargers: " + data["total_chargers"]
        document.getElementById("mqtt-time-2").innerHTML = "Time until arrival: " + data ["time_until_arrival"]
    }
    // document.getElementById("mqtt-data").innerHTML = message.payloadString;
}
