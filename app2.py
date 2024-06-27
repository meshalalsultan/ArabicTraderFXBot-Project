from pyrogram import Client, filters
from openai import OpenAI
import os
import json
import time
import openai


# Retrieve OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Create a new bot instance
app = Client("ArabicTraderFXbot", api_id="api_id", api_hash="api_hash", bot_token="bot_token")

def market_analysis(stock_or_pair):
    # Dummy implementation for market analysis
    return f"تحليل السوق لـ {stock_or_pair} يظهر اتجاهًا إيجابيًا."

def sentiment_analysis(stock_or_pair):
    # Dummy implementation for sentiment analysis
    return f"تحليل الشعور لـ {stock_or_pair} إيجابي بشكل عام."

def technical_analysis(stock_or_pair):
    # Dummy implementation for technical analysis
    return f"التحليل الفني لـ {stock_or_pair} يشير إلى إشارة شراء قوية."

def risk_management():
    # Dummy implementation for risk management advice
    return "ننصح بتحديد أوامر وقف الخسارة وإدارة المخاطر بحذر."

def educational_content(topic):
    # Dummy implementation for educational content
    return f"شرح مبسط لـ {topic}."

def personalized_insights(user_info):
    # Dummy implementation for personalized insights
    return "توصيات مخصصة بناءً على أسلوب التداول الخاص بك وأهدافك."

def create_chat_completion(query, functions):
    messages = [
        {
            "role": "system",
            "content": (
                "أنت TraderGPT، مساعد AI مصمم لمساعدة المتداولين العرب في أسواق الأسهم والفوركس. "
                "هدفك هو تقديم رؤى قيمة، ومحتوى تعليمي، ونصائح شخصية لتحسين قرارات التداول الخاصة بهم. "
                "فيما يلي كيف يمكنك المساعدة:\n"
                "1. تحليل السوق\n"
                "2. التحليل الفني\n"
                "3. تحليل المشاعر\n"
                "4. إدارة المخاطر\n"
                "5. محتوى تعليمي\n"
                "6. رؤى مخصصة\n"
                "7. دعم في الوقت الحقيقي\n"
                "استخدم اللغة العربية الواضحة والبسيطة لضمان سهولة الفهم."
            )
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = client.chat.completions.create(model="gpt-4",
    messages=messages,
    functions=functions,
    function_call="auto")
    return response

@app.on_message(filters.command("ask"))
def handle_query(client, message):
    query = " ".join(message.command[1:])
    if not query:
        message.reply_text("يرجى تقديم استفسار بعد الأمر /ask.")
        return

    functions = [
        {
            "name": "market_analysis",
            "description": "تحليل السوق لأسهم أو أزواج العملات",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_or_pair": {"type": "string", "description": "رمز السهم أو الزوج، مثل AAPL"}
                },
                "required": ["stock_or_pair"]
            }
        },
        {
            "name": "sentiment_analysis",
            "description": "تحليل الشعور لأسهم أو أزواج العملات",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_or_pair": {"type": "string", "description": "رمز السهم أو الزوج، مثل AAPL"}
                },
                "required": ["stock_or_pair"]
            }
        },
        {
            "name": "technical_analysis",
            "description": "تحليل فني لأسهم أو أزواج العملات",
            "parameters": {
                "type": "object",
                "properties": {
                    "stock_or_pair": {"type": "string", "description": "رمز السهم أو الزوج، مثل AAPL"}
                },
                "required": ["stock_or_pair"]
            }
        },
        {
            "name": "risk_management",
            "description": "نصائح لإدارة المخاطر في التداول",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        },
        {
            "name": "educational_content",
            "description": "محتوى تعليمي لمساعدة المتداولين",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "موضوع تعليمي، مثل التحليل الفني"}
                },
                "required": ["topic"]
            }
        },
        {
            "name": "personalized_insights",
            "description": "رؤى مخصصة بناءً على معلومات المستخدم",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_info": {"type": "string", "description": "معلومات المستخدم، مثل أسلوب التداول والأهداف"}
                },
                "required": ["user_info"]
            }
        }
    ]

    try:
        response = create_chat_completion(query, functions)
        print("ChatCompletion response received")
    except Exception as e:
        print(f"Error during ChatCompletion: {e}")
        message.reply_text("حدث خطأ أثناء معالجة الطلب. يرجى المحاولة مرة أخرى لاحقًا.")
        return

    choices = response.choices[0]
    if choices.finish_reason == "function_call":
        function_call = choices.message.function_call
        function_name = function_call.name
        arguments = json.loads(function_call.arguments)
        print(f"Function called: {function_name} with arguments: {arguments}")
        
        try:
            if function_name == "market_analysis":
                result = market_analysis(**arguments)
            elif function_name == "sentiment_analysis":
                result = sentiment_analysis(**arguments)
            elif function_name == "technical_analysis":
                result = technical_analysis(**arguments)
            elif function_name == "risk_management":
                result = risk_management()
            elif function_name == "educational_content":
                result = educational_content(**arguments)
            elif function_name == "personalized_insights":
                result = personalized_insights(**arguments)
            else:
                result = "لم يتم التعرف على الوظيفة المطلوبة."

            print(f"Function result: {result}")
            message.reply_text(result)
        except Exception as e:
            print(f"Error during function execution: {e}")
            message.reply_text("حدث خطأ أثناء تنفيذ الوظيفة. يرجى المحاولة مرة أخرى لاحقًا.")
    else:
        answer = choices.message.content.strip()
        print(f"Bot response: {answer}")
        message.reply_text(answer)

# Run the bot
print("Running the bot")
app.run()

