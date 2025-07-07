odoo.define('ai_chatbot_odoo.chatbot', function(require){
    "use strict";

    $(document).ready(function(){
        const $chatbot = $(`
            <div id="chatbot-box">
                <div id="chatbot-header">Simbi 🤖</div>
                <div id="chatbot-messages"></div>
                <div id="chatbot-typing"><em>piensando...</em></div>
                <input type="text" id="chatbot-input" placeholder="Escreve algo..." />
            </div>
        `);
        $("body").append($chatbot);
        $("#chatbot-typing").hide();

        $("#chatbot-input").keypress(function(e){
            if (e.which === 13) {
                let question = $(this).val();
                if (!question) return;

                $("#chatbot-messages").append(`<div class="user-msg">${question}</div>`);
                $(this).val("");
                $("#chatbot-typing").show();

                $.ajax({
                    url: "/ai_chatbot/ask",
                    method: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({ question }),
                    success: function(res){
                        $("#chatbot-typing").hide();
                        if (res.answer)
                            $("#chatbot-messages").append(`<div class="bot-msg">${res.answer}</div>`);
                        else
                            $("#chatbot-messages").append(`<div class="bot-msg error">Erro: ${res.error}</div>`);
                    },
                    error: function(){
                        $("#chatbot-typing").hide();
                        $("#chatbot-messages").append(`<div class="bot-msg error">Erro de comunicação com o servidor.</div>`);
                    }
                });
            }
        });
    });
});