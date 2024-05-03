import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

generation_config=genai.types.GenerationConfig(temperature=1.1)
safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]


def generate_script(filename, text):
    print("Generating script...")
    script = ""
    response = model.generate_content(
        f"""Your task is to write a engaging and informative Reddit post that summarizes the key points and findings from the provided academic text. The goal is to make the content accessible and interesting for a general audience, while still capturing the essential details and significance of the research.
        If the text is a machine learning paper that proposes a new model architecture, you should devote a substantial portion of the post to explaining the model in clear, easy-to-understand terms. Describe the high-level architecture, the key components and how they work together, and the innovative aspects that make this model unique or superior to previous approaches. Use analogies, diagrams, or other visual aids to help readers grasp the technical details.
        For other types of academic texts, your post should provide a concise yet comprehensive overview of the paper's objectives, methodology, results, and conclusions. Highlight the most important takeaways and explain why this research is meaningful or impactful within the field. Draw connections to real-world applications or implications that would be relevant and interesting to the target subreddit audience.
        Throughout the post, aim to strike a balance between scientific rigor and engaging, accessible language. Avoid jargon when possible, and use vivid descriptions, relatable examples, and a conversational tone to keep readers hooked. Feel free to inject your own enthusiasm for the topic and speculate on future directions or open questions stemming from the work. IT IS A REDDIT POST.
        Remember, the goal is to spark discussion and interest within the subreddit community. End your post with a call-to-action, inviting readers to share their thoughts, ask questions, or explore the topic further. You want this to be a post that people will genuinely enjoy reading and feel compelled to engage with. DO NOT USE MARKDOWN, DO NOT USE POINTS, ONLY USE PLAIN TEXT.
        TEXT:{text}"""
    )
    response.resolve()
    for candidate in response.candidates:
        for part in candidate.content.parts:
            script += part.text

    with open(f"{filename}", "w", encoding="utf-8") as file:
        file.write(script)
    
    print(f"Script saved to {filename}")
    return script