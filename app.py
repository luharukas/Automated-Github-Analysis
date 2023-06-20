# Import all the important libraries and frameworks
from flask import Flask, render_template,request
from src.utils import *
from src.userinfo import userInfo
import yaml
import os
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from tqdm.auto import tqdm
from langchain.vectorstores import Chroma


# Set environment tokens
with open('src/credentials.yml',"r") as file:
    tokens=yaml.safe_load(file)
os.environ['OPENAI_API_KEY']=tokens['OPENAI_API_KEY']


app = Flask(__name__)
embeddings = OpenAIEmbeddings(disallowed_special=())
model = ChatOpenAI(model_name="gpt-3.5-turbo",)  # 'ada' 'gpt-3.5-turbo' 'gpt-4',


# Routing 
@app.route('/')
def home():
    return render_template('index.html')

# Routing when there is query from the UI (Please put the github token ID and OPENAI API key in credential.yml file)
@app.route('/start',methods=['GET','POST'])
def start():

    if request.method=='POST':

        # validity of url
        url=request.form.get('url')
        result=validate_github_url(url)

        if result:
            user=userInfo(url)
            
            if user.get_user_repositories():

                if user.repo_length==0:
                    return render_template('index.html',result="No Public Repository Found")
                else:
                    try:
                        document_list=[]
                        for repo in tqdm(user.repo_name()):
                            try:
                                repo_content=user.get_repository_content(repo)
                                # repo_content=reduce_token_size(user.get_repository_content(repo))
                                document_list.append(Document(page_content=repo_content,metadata={'reponame':repo}))
                            except:
                                continue
                        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
                            chunk_size=1000, chunk_overlap=0,
                        )

                        texts = text_splitter.split_documents(document_list)
                        print("Splitting done")
                        db=Chroma.from_documents(texts,embeddings)
                        print("Insertion  and loading in db complete")
                        retriever = db.as_retriever()
                        retriever.search_kwargs["distance_metric"] = "cos"
                        retriever.search_kwargs["fetch_k"] = 200
                        retriever.search_kwargs["maximal_marginal_relevance"] = True
                        retriever.search_kwargs["k"] = 5
                        print("Database as retrivver")
                        qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)
                        print("Conversation retrival chain")
                        question="Your task is to analyze all the script understand its work and tell me which script is more technically complex and challenging based on parameters like code complexity, usefulness, length, code structure, code quality etc. Return only repo  name as result. t should be in the formatof 'Result:\{repo_name\}\n Description: \{descrition of the project\}'"
                        result = qa({"question": question, "chat_history":[]})

                        return render_template('index.html',result=f"Response: {result['answer']}")
                    
                    except Exception as e:
                        return render_template('index.html',result=f"Something is wrong\n {e}")
            else:
                return render_template('index.html',result="Problem in fetching repository from the URL")
        
        else:
            return render_template('index.html',result="Not a correct URL. Please enter url in the format of https://www.github.com/username")
        
    return render_template('index.html',result="Methods not allowed",)


# Main Function
if __name__ == '__main__':
    app.run(debug=False)