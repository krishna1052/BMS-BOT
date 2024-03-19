#milvus vectorstore
#connect to local mivus vectorstore and query vectors
from pymilvus import connections, Collection
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.agents import tool
class KnowledgeBase():
    def __init__(self, host='localhost', port='19530', collection_name='bmsce_information'):
        connections.connect(host=host, port=port)
        self.collection = Collection(collection_name)
        self.collection.load()
        
    # @tool
    def get_context(self, user_input: str) -> str:
        """Function to get context about B.M.S. College of Engineering from the knowledge base"""
        search_params = {
            "metric_type": "L2", 
            "offset": 0, 
            "ignore_growing": False, 
            "params": {"nprobe": 10}
        }
        user_input_vector = HuggingFaceEmbeddings().embed_documents([user_input])
        kb_response = self.collection.search(data=[user_input_vector[0]], anns_field="embedding", limit=3, param=search_params, output_fields=["link", "content", "tags"])
        print("context: ", kb_response[0][0].entity.get("content"))
        return kb_response[0][0].entity.get("content")