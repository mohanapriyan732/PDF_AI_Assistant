import os

os.environ["HF_HOME"] = "./hf_cache"
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"


from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain.chat_models import init_chat_model


# -------------------------
# Environment
# -------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise Exception("Google API key missing")


# -------------------------
# Flask
# -------------------------

app = Flask(__name__)

CORS(app)


# -------------------------
# Paths
# -------------------------

PDF_PATH = "./Attention_is_all_you_need.pdf"

DB_PATH = "./chroma_langchain_db"


# -------------------------
# Load PDF
# -------------------------

def load_pdf():

    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(
            "PDF file not found"
        )


    loader = PyPDFLoader(PDF_PATH)

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200

    )

    chunks = splitter.split_documents(documents)


    return chunks



# -------------------------
# Vector Database
# -------------------------

embeddings = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-mpnet-base-v2"

)



vector_store = Chroma(

    collection_name="pdf_assistant",

    embedding_function=embeddings,

    persist_directory=DB_PATH

)



# Add PDF only first time

if os.path.exists(DB_PATH):

    print("Creating database...")

    chunks = load_pdf()

    vector_store.add_documents(chunks)

    print("Database created")

else:

    print("Database loaded")




# -------------------------
# Gemini Model
# -------------------------

model = init_chat_model(

    "google_genai:gemini-2.5-flash",

    api_key=GOOGLE_API_KEY

)



# -------------------------
# RAG Functions
# -------------------------


def retrieve_context(question):

    docs = vector_store.similarity_search(

        question,

        k=4

    )


    context = ""


    for doc in docs:

        context += (

            doc.page_content

            + "\n\n"

        )


    return context



def ask_pdf(question):


    context = retrieve_context(question)


    prompt = f"""

You are a PDF AI assistant.

Answer only using this context.

If the answer is not present,
say:
"I cannot find this in the document."

Context:

{context}

Question:

{question}

"""


    response = model.invoke(prompt)


    return response.content



# -------------------------
# Routes
# -------------------------


@app.route("/")
def home():

    return render_template("index.html")



@app.route("/ask", methods=["POST"])
def ask():


    try:

        data = request.get_json()


        question = data.get("question")


        if not question:

            return jsonify({

                "error":"Question required"

            }),400



        answer = ask_pdf(question)



        return jsonify({

            "answer":answer

        })



    except Exception as e:


        return jsonify({

            "error":str(e)

        }),500




# -------------------------
# Run
# -------------------------

if __name__ == "__main__":

    app.run(

        debug=True

    )