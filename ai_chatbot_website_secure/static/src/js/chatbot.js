document.addEventListener('DOMContentLoaded', function() {
    console.log("✅ chatbot.js (versão segura) carregado com sucesso!");

    const toggleButton = document.getElementById('chatbot-toggle-button');
    let chatbotBox = null;
    let typingIndicator = null;
    let inputField = null;
    let messageContainer = null;

    function renderChatbotBox() {
        if (!chatbotBox) {
            chatbotBox = document.createElement("div");
            chatbotBox.id = "chatbot-box";
            chatbotBox.style.cssText = `
                display: none;
                position: fixed;
                bottom: 90px;
                right: 20px;
                width: 350px;
                height: 450px;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.4);
                z-index: 9999;
                flex-direction: column;
                overflow: hidden;
            `;
            chatbotBox.innerHTML = `
                <div id="chatbot-header" style="
                    background-color: #007bff;
                    color: white;
                    padding: 10px;
                    border-top-left-radius: 9px;
                    border-top-right-radius: 9px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <span>Simbi 🤖</span>
                    <button id="chatbot-inline-close-button" style="
                        background: none;
                        border: none;
                        color: white;
                        font-size: 20px;
                        cursor: pointer;
                    ">
                        X
                    </button>
                </div>
                <div id="chatbot-messages-container" style="
                    flex-grow: 1;
                    padding: 10px;
                    overflow-y: auto;
                    background-color: #f9f9f9;
                "></div>
                <div id="chatbot-typing" style="
                    padding: 5px 10px;
                    font-style: italic;
                    color: #666;
                    text-align: center;
                    display: none;
                ">
                    <em>piensando...</em>
                </div>
                <div style="
                    padding: 10px;
                    border-top: 1px solid #eee;
                    display: flex;
                ">
                    <input type="text" id="chatbot-input" placeholder="Escreve algo..." style="
                        flex-grow: 1;
                        padding: 8px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        margin-right: 10px;
                    "/>
                    <button id="chatbot-send-button" style="
                        background-color: #28a745;
                        color: white;
                        border: none;
                        padding: 8px 15px;
                        border-radius: 5px;
                        cursor: pointer;
                    ">
                        Enviar
                    </button>
                </div>
            `;
            document.body.appendChild(chatbotBox);

            typingIndicator = document.getElementById("chatbot-typing");
            inputField = document.getElementById("chatbot-input");
            messageContainer = document.getElementById("chatbot-messages-container");
            const sendButton = document.getElementById("chatbot-send-button");
            const closeButton = document.getElementById("chatbot-inline-close-button");

            inputField.addEventListener("keypress", (e) => {
                if (e.key === "Enter") handleInput();
            });
            sendButton.addEventListener("click", handleInput);
            closeButton.addEventListener("click", toggleChatbotVisibility);
        }
    }

    function toggleChatbotVisibility() {
        renderChatbotBox();
        if (chatbotBox.style.display === 'none' || chatbotBox.style.display === '') {
            chatbotBox.style.display = 'flex';
            toggleButton.textContent = '✖️';
            toggleButton.style.backgroundColor = '#dc3545';
        } else {
            chatbotBox.style.display = 'none';
            toggleButton.textContent = '💬';
            toggleButton.style.backgroundColor = '#007bff';
        }
    }

    function handleInput() {
        const question = inputField.value.trim();
        if (!question) return;

        const userMsg = document.createElement("div");
        userMsg.className = "user-msg";
        userMsg.style.cssText = `
            margin-bottom: 5px;
            text-align: right;
            background-color: #e0f7fa;
            padding: 8px;
            border-radius: 5px;
            max-width: 80%;
            margin-left: auto;
        `;
        userMsg.textContent = question;
        messageContainer.appendChild(userMsg);

        inputField.value = "";
        typingIndicator.style.display = "block";
        messageContainer.scrollTop = messageContainer.scrollHeight;

        fetch("/ai_chatbot/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            typingIndicator.style.display = "none";
            const botMsg = document.createElement("div");
            botMsg.className = "bot-msg";
            botMsg.style.cssText = `
                margin-bottom: 5px;
                text-align: left;
                background-color: #f1f0f0;
                padding: 8px;
                border-radius: 5px;
                max-width: 80%;
                margin-right: auto;
            `;
            botMsg.textContent = data?.result?.answer || "Resposta inválida";
            messageContainer.appendChild(botMsg);
            messageContainer.scrollTop = messageContainer.scrollHeight;
        })
        .catch(error => {
            typingIndicator.style.display = "none";
            const errorMsg = document.createElement("div");
            errorMsg.className = "bot-msg error";
            errorMsg.style.cssText = `
                margin-bottom: 5px;
                text-align: left;
                background-color: #ffe0e0;
                padding: 8px;
                border-radius: 5px;
                max-width: 80%;
                margin-right: auto;
                color: #d32f2f;
            `;
            errorMsg.textContent = "Erro ao comunicar com o servidor.";
            messageContainer.appendChild(errorMsg);
            messageContainer.scrollTop = messageContainer.scrollHeight;
        });
    }

    if (toggleButton) {
        toggleButton.addEventListener('click', toggleChatbotVisibility);
    }
});
