import random

# Load dataset into dictionary
def load_dataset(file_path):
    qa_pairs = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 2:
                question, answer = parts
                qa_pairs[question.lower()] = answer
    return qa_pairs

# Chatbot response function
def chatbot_response(user_input, qa_pairs):
    user_input = user_input.lower().strip()
    return qa_pairs.get(user_input, "Sorry, I don't understand that.")

if __name__ == "__main__":
    qa_pairs = load_dataset("dataset.txt")
    print("Chatbot is ready! Type 'bye' to exit.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye!")
            break
        response = chatbot_response(user_input, qa_pairs)
        print("Chatbot:", response)
