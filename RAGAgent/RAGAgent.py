from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from pathlib import Path
import os
from joblib import dump, load

class RAGAgent:
    def __init__(self, 
                 csv_file: str = "RAGdata/monuments.csv",
                 processed_dir: str = "RAGdata/processed"):
        self._embeddings = None
        self._db = None

        # Add memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chat_history = []

        # File paths
        self.csv_file = csv_file
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache files
        self.embedding_file = self.processed_dir / "embeddings.pkl"
        self.chunks_file = self.processed_dir / "chunks.pkl"
        self.faiss_index_dir = self.processed_dir / "faiss_index"
        
        # Track saved states
        self.embeddings_saved = False
        self.chunks_saved = False
        self.faiss_index_saved = False
        
        # Initialize prompt template for monuments
        self.PROMPT_TEMPLATE = """You are an expert local tour guide with deep knowledge about monuments and temples. Your task is to provide accurate information based STRICTLY on the context provided. 

RULES:
1. ONLY use information explicitly stated in the context
2. If information about any aspect is not in the context, skip that section"
3. Do not make assumptions or add information from general knowledge
4. If the question is about a different monument than those mentioned in the context, say "I don't have information about that monument in my current knowledge base"

Context: {context}

Question: {question}

Format your response in the following structure:
1. **Name and Location:** 
2. **Historical Background:** 
3. **Architectural Features:** 
4. **Cultural and Religious Significance:** 
5. **Current Status and Additional Information:**

Remember: Only include sections where you have explicit information from the context. Skip sections where you don't have information rather than making assumptions. Try to keep the response under 200 words."""

        self.prompt = PromptTemplate(
            template=self.PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )

    @property
    def embeddings(self):
        if self._embeddings is None:
            if os.path.exists(self.embedding_file):
                with open(self.embedding_file, "rb") as f:
                    self._embeddings = load(f)
                self.embeddings_saved = True
            else:
                self._embeddings = HuggingFaceEmbeddings(
                    model_name="BAAI/bge-large-en-v1.5"
                )
                with open(self.embedding_file, "wb") as f:
                    dump(self._embeddings, f)
        return self._embeddings

    @property
    def db(self):
        if self._db is None:
            self._db = self.load_and_chunk_documents()
        return self._db

    def load_and_chunk_documents(self):
        """Load documents from CSV, chunk them, and create FAISS index."""
        chunks = None
        
        # Load cached chunks if available
        if os.path.exists(self.chunks_file):
            with open(self.chunks_file, "rb") as f:
                chunks = load(f)
            self.chunks_saved = True
        
        # Load and process documents if needed
        if not self.chunks_saved:
            loader = CSVLoader(file_path=self.csv_file)
            data = loader.load()
            
            # Chunk documents
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50
            )
            chunks = text_splitter.split_documents(data)


            def monument_aware_chunking(data):
                """Custom chunking that preserves monument information structure"""
                chunks = []
                for doc in data:
                    # Extract CSV fields
                    metadata = doc.metadata # Metadata is a dictionary 
                    name = doc.metadata.get('name', '')
                    
                    # Create separate chunks for major sections while preserving metadata
                    sections = [
                        "Historical Background", 
                        "Architectural Features",
                        "Religious Significance", 
                        "Current Status"
                    ]
                    
                    content = doc.page_content
                    for i, section in enumerate(sections):
                        if i < len(sections) - 1:
                            start = content.find(section)
                            end = content.find(sections[i+1])
                            if start != -1 and end != -1:
                                section_text = content[start:end]
                                chunk_metadata = doc.metadata.copy()
                                chunk_metadata['section'] = section
                                chunks.append(Document(page_content=section_text, metadata=chunk_metadata))
                
                return chunks
            
            # Save chunks
            with open(self.chunks_file, "wb") as f:
                dump(chunks, f)
        
        # Load or create FAISS index
        if os.path.exists(self.faiss_index_dir):
            db = FAISS.load_local(
                str(self.faiss_index_dir),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            self.faiss_index_saved = True
        else:
            db = FAISS.from_documents(chunks, self.embeddings)
            db.save_local(str(self.faiss_index_dir))
        
        return db

    def get_relevant_context(self, query: str, num_docs: int = 3, min_score: float = 0.8) -> str:
        """Retrieve most relevant context for a query, with stricter filtering."""
        # Get documents with similarity scores
        docs_and_scores = self.db.similarity_search_with_score(query, k=num_docs)
        
        # Filter by similarity score and take only most relevant parts
        filtered_docs = []
        for doc, score in docs_and_scores:
            if score >= min_score:
                # Extandract only the most relevant sentences
                sentences = doc.page_content.split('.')
                relevant_sentences = [s.strip() + '.' for s in sentences[:3]]  # Take only first 3 sentences
                filtered_docs.append(' '.join(relevant_sentences))
        
        # If no documents meet the threshold
        if not filtered_docs:
            return ""
            
        return "\n\n".join(filtered_docs)

    def get_rag_prompt(self, query: str) -> str:
        """Get RAG-enhanced prompt for a query."""
        context = self.get_relevant_context(query)
        history = self.memory.load_memory_variables({})
        chat_history = history.get("chat_history", "")
        # Check if the exact query (ignoring case) is present in the retrieved context.
        if not context:
            self.memory.save_context(
                {"input": query},
                {"output": "I don't have information about this in my knowledge base."}
            )
            return (
                f"I apologize, but I don't have any information about {query} in my current knowledge base. "
                "I can only provide information about monuments that are explicitly mentioned in my reference materials."
            )
        # Second pass to ensure relevant response
        if query.lower() not in context.lower():
            return (
                f"I apologize, but I don't have any information about {query} in my current knowledge base. "
                "I can only provide information about monuments that are explicitly mentioned in my reference materials."
            )

    
        enhanced_prompt = self.prompt.format(
            context=context,
            question=query,
            chat_history=chat_history
        )
        print(enhanced_prompt)

        return enhanced_prompt

    def add_to_history(self, query: str, response: str):
        """Add a query-response pair to the chat history."""
        self.memory.save_context(
            {"input": query},
            {"output": response}
        )
        self.chat_history.extend([
            HumanMessage(content=query),
            AIMessage(content=response)
        ])

    def clear_history(self):
        """Clear the chat history."""
        self.memory.clear()
        self.chat_history = []

    def initialize_index(self):
        """Force initialization/reinitialization of the FAISS index."""
        self._db = self.load_and_chunk_documents()
        return True