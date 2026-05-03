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
    const rawText = userInput.value.trim();
    if (rawText === '') return;

    const message = rawText.toLowerCase();

    addUserMessage(rawText);
    userInput.value = '';
    showTypingIndicator();

    setTimeout(() => {
        hideTypingIndicator();
        const response = getBotResponse(message);
        addBotMessage(response);
    }, 700);
}

function addUserMessage(text) {
    const chatMessages = document.getElementById('chatmessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-bubble message-user';
    messageDiv.innerHTML = `
        <div class="message-content">${text}</div>
        <div class="message-meta">You · ${getTimeStamp()}</div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addBotMessage(text) {
    const chatMessages = document.getElementById('chatmessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message-bubble message-bot';
    messageDiv.innerHTML = `
        <div class="message-content">${text}</div>
        <div class="message-meta">Bot · ${getTimeStamp()}</div>
    `;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.remove('d-none');
    }
}

function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.add('d-none');
    }
}

function getTimeStamp() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
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
    if (message.includes('price') || message.includes('cost') || message.includes('amount')) {
        return 'Our kitchen mixers start from ₹1500. For specific models, please visit our products page! 💰';
    }
    if (message.includes('delivery') || message.includes('arrival') || message.includes('days') || message.includes('shipping')) {
        return 'Delivery usually takes 3–7 days depending on your location. 🚚';
    }
    if (message.includes('track') || message.includes('tracking') || message.includes('order status') || message.includes('status')) {
        return 'You can track your order in your profile dashboard under \'My Orders\'.';
    }
    if (message.includes('repair') || message.includes('request repair') || message.includes('service')) {
        return 'Go to Repair section, fill the form, and submit your request. We will contact you shortly. 🔧';
    }
    if (message.includes('payment') || message.includes('methods') || message.includes('cash') || message.includes('pay')) {
        return 'Currently, we support Cash on Delivery. 💵';
    }
    if (message.includes('contact') || message.includes('phone') || message.includes('reach')) {
        return 'You can contact us through the contact form or phone number available on website. ☎️';
    }
    if (message.includes('order') || message.includes('buy') || message.includes('how to order')) {
        return 'To order, visit our products page, select your mixer, and click "Add to Cart". We deliver within 2-3 days! 🛒';
    }
    if (message.includes('warranty')) {
        return 'All our products come with 1-year warranty. Register your product online for extended coverage! 📄';
    }
    if (message.includes('location') || message.includes('where')) {
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
orders, delivery, repair, or contact`;
    }

    // 5. Default response
    return `I'm sorry, I didn't understand that. Please try asking about orders, delivery, repair, or contact.`;
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