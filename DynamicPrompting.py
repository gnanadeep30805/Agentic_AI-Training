from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Explain about {topic} in simple terms for a {audience}."
)

formatted_prompt = prompt.invoke(
    {
        "topic": "quantum computing",
        "audience": "high school student"
    }
)

print(formatted_prompt)