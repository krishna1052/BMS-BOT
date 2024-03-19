from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from bot.knowledgebase import KnowledgeBase

class ChatBot():
    def __init__(self, user):
        self.kb = KnowledgeBase()
        self.model = ChatOllama(temperature=0, model="example")
        self.user_name = user["name"]
        self.tools = [self.kb.get_context]
        self.chat_history = []
        # self.prompt = PromptTemplate(
        #     template="You are BMS-BOT, a friendly AI assistant for B.M.S. College of engineering. Greet the user who is {user_name} Answer all questions concisely and to the point. Chat History: {chat_history} user: {input} context: {context}",
            
        #     input_variables=["user_name", "input", "context"],
        # )
        self.prompt = PromptTemplate(
            template="[INST]You are Seemanthini, a friendly AI assistant for B.M.S. College of engineering. If starting the conversation (no chat_history), greet the user who is {user_name}. Answer all questions concisely and to the point. Chat History: {chat_history} user: {input} context: {context}[/INST]",
            input_variables=["user_name","chat_history", "input", "context"],
        )
        self.chain = self.prompt | self.model |  StrOutputParser()
    
    def get_response(self, user_input="", context_needed=False):
        if context_needed:
            context = self.kb.get_context(user_input)
            response =  self.chain.invoke({"user_name": self.user_name, "chat_history":str(self.chat_history), "input": user_input, "context": context})
            self.extend_chat_history(user_input, response)
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