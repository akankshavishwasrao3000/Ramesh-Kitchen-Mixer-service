// Simple rule-based chatbot for Ramesh Kitchen Mixer
function toggleChat() {
    const chatbox = document.getElementById('chatbox');
    chatbox.style.display = chatbox.style.display === 'none' ? 'block' : 'none';
}

function handleKey(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const userInput = document.getElementById('userinput');
    const message = userInput.value.trim().toLowerCase();
    if (message === '') return;

    // Add user message to chat
    addMessage('You: ' + userInput.value);

    // Process the message
    const response = getBotResponse(message);
    addMessage('Bot: ' + response);

    // Clear input
    userInput.value = '';
}

function addMessage(text) {
    const chatMessages = document.getElementById('chatmessages');
    const messageDiv = document.createElement('div');
    messageDiv.innerHTML = text.replace(/\n/g, '<br>');
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getBotResponse(message) {
    // 1. Check for greetings FIRST
    const greetings = ['hi', 'hello', 'hey', 'good morning', 'good evening', 'good afternoon'];
    for (let greeting of greetings) {
        if (message.startsWith(greeting) || message === greeting) {
            return `Hello 👋 Welcome to Ramesh Kitchen Mixer!<br>
I am your AI assistant 😊<br><br>
You can ask me:<br>
• Product price 💰<br>
• How to order 🛒<br>
• Repair service 🔧<br>
• Warranty 📄<br>
• Shop location 📍`;
        }
    }

    // 2. Check for known queries
    if (message.includes('price')) {
        return 'Our kitchen mixers start from ₹1500. For specific models, please visit our products page! 💰';
    }
    if (message.includes('order')) {
        return 'To order, visit our products page, select your mixer, and click "Add to Cart". We deliver within 2-3 days! 🛒';
    }
    if (message.includes('repair')) {
        return 'For repairs, contact us at +91-9876543210 or visit our service center. We offer doorstep service! 🔧';
    }
    if (message.includes('warranty')) {
        return 'All our products come with 1-year warranty. Register your product online for extended coverage! 📄';
    }
    if (message.includes('location')) {
        return 'We are located at 123 Main Street, City Center. Open 9 AM to 9 PM daily! 📍';
    }

    // 3. Check for thanks or bye
    if (message.includes('thank') || message.includes('bye')) {
        return 'You\'re welcome! 😊 Have a great day!';
    }

    // 4. Fallback for short or random messages
    if (message.length < 2 || !/[a-zA-Z]/.test(message)) {
        return `Sorry 😅 I didn’t understand that.<br>
Please type something like:<br>
price, order, repair, warranty, location`;
    }

    // 5. Default response
    return `I'm here to help! 😊<br>
Ask me about:<br>
• Product price 💰<br>
• How to order 🛒<br>
• Repair service 🔧<br>
• Warranty 📄<br>
• Shop location 📍`;
}

// Services page scroll animations
document.addEventListener('DOMContentLoaded', function () {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Animate feature and service cards on services page
    document.querySelectorAll('.feature-card, .service-card').forEach(card => {
        if (card) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.6s, transform 0.6s';
            observer.observe(card);
        }
    });
});