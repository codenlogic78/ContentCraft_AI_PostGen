from llm_helper import llm
from few_shot import FewShotPosts
from config import Config

config = Config()
few_shot = FewShotPosts()


def get_length_str(length):
    """Convert length option to descriptive string"""
    return config.LENGTH_MAPPING.get(length, "6 to 10 lines")


def generate_post(length, language, tag):
    """Generate a social media post based on specified parameters"""
    try:
        prompt = get_prompt(length, language, tag)
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating post: {str(e)}. Please check your API configuration."


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate an engaging social media post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    
    Guidelines:
    - Create authentic, engaging content that resonates with the audience
    - If Language is Hinglish, use a natural mix of Hindi and English with English script
    - Focus on providing value, insights, or inspiration related to the topic
    - Use a conversational tone that feels personal and genuine
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))