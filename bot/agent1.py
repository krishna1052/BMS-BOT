
from pymilvus import connections, Collection
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import tool, AgentExecutor
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain_core.messages import AIMessage, HumanMessage
#query
@tool
def get_context(user_input: str) -> str:
    """Function to get context about B.M.S. College of Engineering from the knowledge base, based on user input."""
    connections.connect(host="localhost", port="19530")
    collection = Collection("bmsce_information")
    collection.load()
    search_params = {
        "metric_type": "L2", 
        "offset": 0, 
        "ignore_growing": False, 
        "params": {"nprobe": 10}
    }
    user_input_vector = HuggingFaceEmbeddings().embed_documents([user_input])
    kb_response = collection.search(data=[user_input_vector[0]], anns_field="embedding", limit=3, param=search_params, output_fields=["link", "content", "tags"])
    print("context: ", kb_response[0][0].entity.get("content"))
    return kb_response[0][0].entity.get("content")

class ChatBot():
    def __init__(self):
        self.model = ChatOpenAI(base_url = "http://localhost:11434/v1", api_key = "ollama", temperature=0, model="nous-hermes")
        self.tools = [get_context]
        self.chat_history = []
        self.model_with_tools = self.model.bind_tools(self.tools)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"You are BMS-BOT, a friendly AI assistant for B.M.S. College of engineering. Greet the user who is Adithya. Answer all questions after taking in context from the knowledge base, (using tool) for B.M.S College of Engineering related questions. You will make use of the tools provided for every query. ",
                ),
                MessagesPlaceholder(variable_name="self.chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        self.agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
                "self.chat_history": lambda x: x["self.chat_history"],
            }
            | self.prompt
            | self.model_with_tools
            | OpenAIToolsAgentOutputParser()    
        )
        
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
    def extend_chat_history(self, result, user_input):
        self.chat_history.extend([HumanMessage(user_input), AIMessage(result) ])
        return self.chat_history
    def get_chat_history(self):
        return self.chat_history
    def get_response(self, user_input):
        response = self.agent_executor.invoke({"input": user_input, "self.chat_history": self.get_chat_history()})["output"]
        self.extend_chat_history(response, user_input)
        return response
    

if __name__ == "__main__":
    bot = ChatBot()
    print("BOT: " ,bot.get_response("Start the conversation."))
    user_input = input("Type a message:")
    while user_input!="exit":
        result = bot.get_response(user_input)
        print("BOT: ",result)
        user_input = input("Type a message:")