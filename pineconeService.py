from pinecone import Pinecone
import os

class PineconeService:
    def __init__(self):
        self.PINECONE_KEY = os.getenv("PINECONE_KEY")
        self.pinecone = Pinecone(api_key=self.PINECONE_KEY)

    def get_pinecone(self):
        return self.pinecone