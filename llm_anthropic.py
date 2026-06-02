# pip install -U langchain-anthropic
import warnings
warnings.filterwarnings('ignore', message='.*Pydantic V1 functionality.*')

from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    api_key="-ant-api03--MyCxaAAA"
 )

response = model.invoke(" What is the capital of India...")
print(response.content)
