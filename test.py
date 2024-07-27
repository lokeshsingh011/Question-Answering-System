from transformers import pipeline

qa_pipeline = pipeline("question-answering")
result = qa_pipeline(question="What is the capital of France?", context="France, in Western Europe, encompasses medieval cities, alpine villages, and Mediterranean beaches. Its capital, Paris, is famed for its fashion houses, classical art museums including the Louvre and monuments like the Eiffel Tower.")
print(result)
