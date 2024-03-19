from langchain import hub
from langchain.agents import AgentExecutor, tool
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from knowledgebase import KnowledgeBase
from langchain.prompts import PromptTemplate, HumanMessagePromptTemplate

class BMSAgent():
    def __init__(self):
        self.model = ChatOllama(temperature=0, model="llama2")
        self.kb = KnowledgeBase()
        self.tools = [self.kb.get_context]
        self.prompt = dict(
            input_variables=['agent_scratchpad', 'input', 'tools'],
            partial_variables={'chat_history': ''},
            messages= [ HumanMessagePromptTemplate(prompt=PromptTemplate(
                input_variables=['agent_scratchpad', 'chat_history', 'input', 'tools'], 
                template="You are a helpful assistant. Help the user answer any questions.\n\nYou have access to the following tools:\n\n{tools}\n\nIn order to use a tool, you can use <tool></tool> and <tool_input></tool_input> tags. You will then get back a response in the form <observation></observation>\nFor example, if you have a tool called 'get_context' that could query a vectorstore for context given the input, in order to get context for a user query \"Where is BMS located\" you would respond:\n\n<tool>search</tool><tool_input>Where is B.M.S College of engineering located</tool_input>\n<observation>P.O. Box No.: 1908, Bull Temple Road, Bangalore - 560 019 Karnataka, India.</observation>\n\nWhen you are done, respond with a final answer between <final_answer></final_answer>. For example:\n\n<final_answer>The address of B.M.S College of Engineering is: P.O. Box No.: 1908, Bull Temple Road, Bangalore - 560 019 Karnataka, India. </final_answer>\n\nBegin!\n\nPrevious Conversation:\n{chat_history}\n\nQuestion: {input}\n{agent_scratchpad}",
                ))])
        
        self.agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: self.convert_intermediate_steps(x["intermediate_steps"]),
            }
            | self.prompt.partial(tools=convert_tools(self.tools))
            | self.model.bind(stop=["</tool_input>", "</final_answer>"]) 
            | StrOutputParser()
        )
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

def convert_intermediate_steps(intermediate_steps):
    log = ""
    for action, observation in intermediate_steps:
        log += (
            f"<tool>{action.tool}</tool><tool_input>{action.tool_input}</tool_input><observation>{observation}</observation>"
        )
    return f"<intermediate_steps>{log}</intermediate_steps>"

# Logic for converting tools to string to go in prompt
def convert_tools(tools):
    return "\n".join([f"{tool.name}: {tool.description}" for tool in tools])


if __name__ == "__main__":
   agent = BMSAgent()
   print(agent.agent_executor.invoke({"input": "What is the address of BMS College of Engineering?"}))