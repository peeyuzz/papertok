import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
    # response = model.generate_content(
    #     f"""Your task is to write a engaging and informative Reddit post that summarizes the key points and findings from the provided academic text. The goal is to make the content accessible and interesting for a general audience, while still capturing the essential details and significance of the research.
    #     If the text is a machine learning paper that proposes a new model architecture, you should devote a substantial portion of the post to explaining the model in clear, easy-to-understand terms. Describe the high-level architecture, the key components and how they work together, and the innovative aspects that make this model unique or superior to previous approaches. Use analogies, diagrams, or other visual aids to help readers grasp the technical details.
    #     For other types of academic texts, your post should provide a concise yet comprehensive overview of the paper's objectives, methodology, results, and conclusions. Highlight the most important takeaways and explain why this research is meaningful or impactful within the field. Draw connections to real-world applications or implications that would be relevant and interesting to the target subreddit audience.
    #     Throughout the post, aim to strike a balance between scientific rigor and engaging, accessible language. Avoid jargon when possible, and use vivid descriptions, relatable examples, and a conversational tone to keep readers hooked. Feel free to inject your own enthusiasm for the topic and speculate on future directions or open questions stemming from the work. IT IS A REDDIT POST.
    #     Remember, the goal is to spark discussion and interest within the subreddit community. End your post with a call-to-action, inviting readers to share their thoughts, ask questions, or explore the topic further. You want this to be a post that people will genuinely enjoy reading and feel compelled to engage with. DO NOT USE MARKDOWN, DO NOT USE POINTS, ONLY USE PLAIN TEXT.
    #     TEXT:{text}"""
    # )
    response  = model.generate_content(
        f"""
        <PDF TEXT>
        {text}
        </PDF TEXT>

        Write a script (just provide the text the narrator needs to narrate, no need for extra information, dont give me details about the visuals. dont use hashtags or emojis. just a plain .txt of the text the narrator hs to speak) for an engaging TikTok video based on the contents of the provided PDF. The script should be written in a narrator's tone, as if it is being narrated directly to the viewer.
        
        Your script should:

        1. Capture the essence of the PDF in a concise, attention-grabbing manner suitable for TikTok's short-form video format.

        2. Adapt the content based on the PDF type:
        - For a story: Focus on the key plot points, main characters, and central themes.
        - For a research paper: Highlight the main research question, key findings, and potential implications.
        - For an informational document: Emphasize the most important facts, statistics, or concepts.

        3. Structure the script in a way that maintains viewer interest throughout:
        - Start with a hook to grab attention in the first few seconds.
        - Use a clear, logical flow to present information.
        - Include visual cues or transitions that would work well in a TikTok video.

        4. Incorporate elements that make the content more engaging for a TikTok audience:
        - Use conversational language and a friendly tone.
        - Include relevant hashtags where appropriate.
        - Suggest places for popular TikTok sounds or effects, if applicable.

        5. Keep the script length appropriate for TikTok (aim for a 140-200 second video).

        6. End with a strong call-to-action that encourages viewer engagement, such as:
        - Asking viewers to comment with their thoughts or experiences.
        - Suggesting they share the video if they found it informative.
        - Prompting them to follow for more content on similar topics.

        7. Ensure the script is easy to read and perform.

        Remember to maintain the integrity of the original content while making it accessible and entertaining for a TikTok audience. Your goal is to create a script that's informative, engaging, and shareable."""
    )
    response.resolve()
    for candidate in response.candidates:
        for part in candidate.content.parts:
            script += part.text

    with open(f"{filename}", "w", encoding="utf-8") as file:
        file.write(script)
    
    print(f"Script saved to {filename}")
    return script