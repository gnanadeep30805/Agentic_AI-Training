import warnings
warnings.filterwarnings('ignore', message='.*Pydantic V1 functionality.*')

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Gnanadeep_Yenneti.pdf")

docs = loader.load()

print(len(docs))