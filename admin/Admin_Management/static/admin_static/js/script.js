
const roomName = JSON.parse(document.getElementById('room-name').textContent);
const user = JSON.parse(document.getElementById('user').textContent);
const conversation = document.getElementById("conversation");
const sendButton = document.getElementById("send");
const inputField = document.getElementById("comment");

// const chatSocket = new WebSocket("wss://" + window.location.host + "/ws/chat/" + roomName + "/");
const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
const chatSocket = new WebSocket(protocol + window.location.host + "/ws/chat/" + roomName + "/");

document.getElementById("hiddeninput").addEventListener("change", handleFileSelect, false);

function handleFileSelect(event) {
  var fileInput = document.getElementById("hiddeninput");
  var file = fileInput.files[0];

  // Check if a file was selected
  if (!file) {
      console.error("No file selected.");
      return; // Exit if no file is selected
  }

  // Call the function to get the base64 representation of the file
  getBase64(file, file.type);
}

function getBase64(file, fileType) {
  var type = fileType.split("/")[0]; // 'image', 'video', 'audio', etc.
  var reader = new FileReader();

  reader.readAsDataURL(file);

  reader.onload = function() {
      chatSocket.send(JSON.stringify({
          "what_is_it": type, // Send the actual file type
          "message": reader.result
      }));
  };

  reader.onerror = function(error) {
      console.error('Error: ', error); // Handle any errors that occur
  };
}
const startStop = document.getElementById("record");

// Initialize variables to track recording state and store recorded data
let isRecord = false;
let mediaRecorder;
let dataArray = [];
let stream;

// Add click event listener to the record button
startStop.onclick = () => {
  if (isRecord) {
      stopRecord();
      startStop.style = ""; // Reset the button style
      isRecord = false;
  } else {
      startRecord();
      startStop.style = "color: red"; // Change the button style to indicate recording
      isRecord = true;
  }
};

// Function to start recording
function startRecord() {
  navigator.mediaDevices.getUserMedia({ audio: true })
      .then(streamObj => {
          stream = streamObj; // Save the stream object for later use
          mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();
          dataArray = []; // Clear the data array

          // Event handler to collect recorded audio data
          mediaRecorder.ondataavailable = function (e) {
              dataArray.push(e.data);
          };

          // Event handler when the recording is stopped
          mediaRecorder.onstop = function (e) {
              let audioData = new Blob(dataArray, { 'type': 'audio/mp3' });
              dataArray = []; // Clear the data array for the next recording
              getBase64(audioData, audioData.type); // Convert the audio data to Base64

              // Stop all audio tracks in the stream
              stream.getTracks().forEach(track => {
                  if (track.readyState === 'live' && track.kind === 'audio') {
                      track.stop();
                  }
              });
          };
      })
      .catch(err => {
          console.error('The following error occurred: ' + err);
      });
}

// Function to stop recording
function stopRecord() {
  mediaRecorder.stop();
}




chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data)
  const message_type = data.what_is_it

  // Current time ko fetch karna aur format karna
 
  // Message HTML ko create karna aur insert karna

  if (message_type === "text"){
    var message = data.message
  }
  else if(message_type ==="image"){
    var message = `<img width="200" height="200" src="${data.message}">`

  }
  else if (message_type === "audio") {
    var message = `<audio style="width:250px;" controls><source src="${data.message}" type="audio/mpeg">Your browser does not support the audio element.</audio>`;
  } else if (message_type === "video") {
      var message = `<video width="320" height="240" controls><source src="${data.message}" type="video/mp4">Your browser does not support the video tag.</video>`;
  }
  
  if (user === data.user) {
      message = `
      <div class="row message-body">
          <div class="col-sm-12 message-main-sender">
              <div class="sender">
                  <div class="message-text">
                      ${message}
                  </div>
                  <span class="message-time pull-right">
                      ${data.created_date}
                  </span>
              </div>
          </div>
      </div>`;
  } else {
      message = `
      <div class="row message-body">
          <div class="col-sm-12 message-main-receiver">
              <div class="receiver">
                  <div class="message-text">
                      ${message}
                  </div>
                  <span class="message-time pull-right">
                      ${data.created_date}
                  </span>
              </div>
          </div>
      </div>`;
  }

  conversation.innerHTML += message;
  conversation.scrollTop = conversation.scrollHeight;

};

chatSocket.onclose = function(e) {
    console.error("Socket unexpectedly closed.");
};

inputField.focus();

inputField.onkeyup = function(e) {
    if (e.keyCode === 13) {
        sendButton.click();
    }
};

sendButton.onclick = function(e) {
    const message = inputField.value;
    chatSocket.send(JSON.stringify({
      "what_is_it":"text",
      "message": message
    }));
    inputField.value = '';
};

$(function(){
  $(".heading-compose").click(function() {
    $(".side-two").css({
      "left": "0"
    });
  });

  $(".newMessage-back").click(function() {
    $(".side-two").css({
      "left": "-100%"
    });
  });
});


function toggleDropdown() {
  var dropdown = document.getElementById("dropdownMenu");
  if (dropdown.style.display === "none" || dropdown.style.display === "") {
      dropdown.style.display = "block";
  } else {
      dropdown.style.display = "none";
  }
}

// Hide the dropdown if clicked outside
window.onclick = function(event) {
  if (!event.target.matches('.fa-ellipsis-v')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      for (var i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.style.display === "block") {
              openDropdown.style.display = "none";
          }
      }
  }
}
