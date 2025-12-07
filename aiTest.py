from openai import OpenAI

client = OpenAI(api_key="AI-KEY")

def define_word(word: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are a helpful dictionary assistant."},
            {"role": "user", "content": f"Define the word '{word}' in one clear sentence."}
        ]
    )
    
    return response.choices[0].message.content

# --- User input section ---
word = input("Enter a word to define: ")

definition = define_word(word)

print(f"\nDefinition of '{word}':\n{definition}")

