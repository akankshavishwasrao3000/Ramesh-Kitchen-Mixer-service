let chatInitialized = false;

function toggleChat() {
    const chatbox = document.getElementById('chatbox');
    if (!chatbox) return;

    const isOpening = chatbox.style.display === 'none' || chatbox.style.display === '';
    chatbox.style.display = isOpening ? 'block' : 'none';
    const toggleButton = document.getElementById('aiicon');
    if (toggleButton) {
        toggleButton.setAttribute('aria-expanded', String(isOpening));
    }

    if (isOpening && !chatInitialized) {
        chatInitialized = true;
        const chatMessages = document.getElementById('chatmessages');
        if (chatMessages && chatMessages.innerHTML.trim() === '') {
            setTimeout(() => {
                const welcomeMsg = 'Hello 👋 Welcome to Ramesh Kitchen Mixer!<br><br>I can help you with:<br><br>🛒 Product Information<br>🔧 Mixer Repair Services<br>📦 Delivery Information<br>📍 Shop Location<br>📞 Contact Details<br>💬 WhatsApp Support<br><br>How may I assist you today?';
                addBotMessage(welcomeMsg);
            }, 300);
        }
    }
}

function handleKey(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const userInput = document.getElementById('userinput');
    if (!userInput) return;

    const rawText = userInput.value.trim();
    if (rawText === '') return;

    addUserMessage(rawText);
    userInput.value = '';
    showTypingIndicator();

    setTimeout(() => {
        hideTypingIndicator();
        const response = getBotResponse(rawText);
        addBotMessage(response);
    }, 700);
}

function addUserMessage(text) {
    const chatMessages = document.getElementById('chatmessages');
    if (!chatMessages) return;

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
    if (!chatMessages) return;

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
    const msg = message.trim().toLowerCase();
    const hasVowels = /[aeiouy]/.test(msg);
    const unusualLength = msg.length > 20 && !msg.includes(' ');
    const repeatedChar = /(.)\1{4,}/.test(msg);

    if ((!hasVowels && msg.length > 5) || unusualLength || repeatedChar) {
        return "I'm sorry, I couldn't understand that input. 😅 Please ask a question related to our products, repairs, or orders so I can assist you properly!";
    }

    let response = '';

    if (['price', 'cost', 'amount', 'rate', 'how much', 'mrp', 'bucks', 'value'].some(k => msg.includes(k))) {
        response += 'Our premium mixers range from ₹3500 to ₹4550. You can see the specific rates on our Products page.<br><br>';
    }

    if (['detail', 'info', 'spec', 'feature', 'motor', 'watt', 'jar', 'quality', 'good'].some(k => msg.includes(k))) {
        response += 'Ramesh Mixers are built for durability with 900W motors, 3 stainless steel jars, and a 24-month warranty.<br><br>';
    }

    if (['repair', 'fix', 'service', 'working', 'problem', 'broken', 'issue', 'mechanic'].some(k => msg.includes(k))) {
        response += 'We provide expert repair services for mixers. Fill out the Repair Request form on our website and we will guide you through the next step.<br><br>';
    }

    if (['contact', 'phone', 'mobile', 'whatsapp', 'call', 'number', 'reach', 'talk'].some(k => msg.includes(k))) {
        response += 'You can reach us directly at +91 9921071945 or use the WhatsApp contact button on the site.<br><br>';
    }

    if (['location', 'address', 'shop', 'where', 'store', 'place', 'city', 'village', 'belhe'].some(k => msg.includes(k))) {
        response += 'Ramesh Kitchen Mixer is located in Belhe, Maharashtra 412410. You are welcome to visit us during business hours.<br><br>';
    }

    if (['delivery', 'shipping', 'courier', 'send', 'receive', 'home', 'post'].some(k => msg.includes(k))) {
        response += 'We offer local delivery and will confirm the delivery timeline via WhatsApp once your order is placed.<br><br>';
    }

    if (['order', 'place', 'buy', 'purchase', 'shopping', 'cart', 'checkout'].some(k => msg.includes(k))) {
        response += 'To buy, select your favorite model on the Products page and complete the order form. We confirm everything on WhatsApp before finalizing.<br><br>';
    }

    if (response === '') {
        if (['hi', 'hello', 'hey', 'namaste', 'morning', 'evening'].some(k => msg.includes(k))) {
            return 'Hello 👋 Welcome to Ramesh Kitchen Mixer! I can help you with product prices, mixer repairs, delivery details, or our shop location. How may I assist you today?';
        }

        if (['thanks', 'thank you', 'great', 'ok', 'fine'].some(k => msg.includes(k))) {
            return 'You are very welcome! 😊 Let me know if you have any other questions.';
        }

        return 'I can help you with:<br><br>🛒 Product Pricing (₹3500 - ₹4550)<br>🔧 Repair Bookings<br>📦 Delivery Information<br>📍 Shop Address (Belhe)<br>📞 Contact Details<br><br>Please ask your question or select a topic!';
    }

    return response;
}

document.addEventListener('DOMContentLoaded', function () {
    const revealItems = document.querySelectorAll('.reveal-item');
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (prefersReducedMotion) {
        revealItems.forEach(item => item.classList.add('is-visible'));
    } else if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.15,
            rootMargin: '0px 0px -30px 0px'
        });

        revealItems.forEach((item) => observer.observe(item));
    } else {
        revealItems.forEach(item => item.classList.add('is-visible'));
    }

    const dashboardShowreel = document.getElementById('dashboardShowreel');
    if (dashboardShowreel && window.bootstrap?.Carousel) {
        const showreel = window.bootstrap.Carousel.getOrCreateInstance(dashboardShowreel);
        if (prefersReducedMotion) {
            showreel.pause();
        } else {
            showreel.cycle();
        }
    }

});