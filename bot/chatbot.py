from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from bot.knowledgebase import KnowledgeBase

class ChatBot():
    def __init__(self, user):
        self.kb = KnowledgeBase()
        self.model = ChatOllama(temperature=0, model="llama3")
        self.user_name = user["name"]
        # self.tools = [self.kb.get_context]
        self.chat_history = []
        # self.prompt = PromptTemplate(
        #     template="You are BMS-BOT, a friendly AI assistant for B.M.S. College of engineering. Greet the user who is {user_name} Answer all questions concisely and to the point. Chat History: {chat_history} user: {input} context: {context}",
            
        #     input_variables=["user_name", "input", "context"],
        # )
        self.prompt = PromptTemplate(
            template="<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are BMS-BOT, a friendly AI assistant for B.M.S. College of Engineering. You must assist students and teachers by answering their questions, while being helpful and honest. If starting the conversation, greet the user who is {user_name}. \n 1. Answer all questions concisely and to the point. \n 2. If you do not know the answer to a question, respond with \" I do not know the answer to this question, as my database is still being updated with current and accurate information \" \n\n\n\n\n\n\n Previous Chat History with the user: {chat_history}. Use the given chathistory and the extracted context to answer your question.<|eot_id|><|start_header_id|>user<|end_header_id|>{input}\n\n\n\n\n\n The extracted context: {context}<|eot_id|><|start_header_id|>assistant<|end_header_id|> ",
            input_variables=["user_name","chat_history", "input", "context"],
        )
        self.chain = self.prompt | self.model |  StrOutputParser()
    
    def get_response(self, user_input="", context_needed=False):
        if context_needed:
            context = self.kb.get_context(user_input)
            response =  self.chain.invoke({"user_name": self.user_name, "chat_history":str(self.chat_history), "input": user_input, "context": context})
            self.extend_chat_history(user_input, response)
            print("chat history: ",self.chat_history)
            return response
        response =  self.chain.invoke({"user_name": self.user_name,"chat_history":str(self.chat_history), "input": user_input, "context": ""})
        self.extend_chat_history(user_input, response)
        return response
    def extend_chat_history(self, user_input, response):
        self.chat_history.append({"user": user_input, "BMS-BOT": response})
        

if __name__ == "__main__":
    bot = ChatBot()
    kb = KnowledgeBase()
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        user_context = kb.get_context(user_input)
        response = bot.chain.invoke({"input": user_input, "context": user_context})
        #streaming response
        
        print(response, flush=True)