const sendButton = document.getElementById('sendButton');
const messageInput = document.getElementById('messageInput');
const messagesDiv = document.getElementById('messages');

// Function to display a message
function displayMessage(sender, message) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = `${sender === 'passenger' ? 'Passenger' : 'Driver'}: ${message}`;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight; // Scroll to the bottom
}

// Function to send a message
sendButton.addEventListener('click', () => {
    const message = messageInput.value.trim();
    if (message) {
        displayMessage('passenger', message);
        messageInput.value = '';

        // Simulating sending message to backend
        fetch('https://major-ghosts-boil.loca.lt/api/sendMessage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ sender: 'passenger', message }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Message sent:', data);
        })
        .catch(error => {
            console.error('Error sending message:', error);
        });
    }
});

// Example function to simulate receiving a message from the driver
function receiveMessageFromDriver(message) {
    displayMessage('driver', message);
}

// Simulate receiving a message after 5 seconds (for demonstration)
setTimeout(() => {
    receiveMessageFromDriver("I'm on my way!");
}, 5000);
