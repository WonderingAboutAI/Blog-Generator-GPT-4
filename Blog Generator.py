import csv
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
print("Environment variables loaded.")

# Initialize the OpenAI client
client = OpenAI()

# Define the path to the supporting text file inside the script
supporting_text_path = 'content.txt'

def generate_blog_post(supporting_text_path):
    # Use the API key from the environment variables
    client.api_key = os.getenv('OPENAI_API_KEY')
    if client.api_key:
        print("API key loaded successfully.")
    else:
        print("Error loading API key. Please check your .env file.")
        return

    # Load supporting content from the text file
    supporting_content = ""
    if supporting_text_path:
        try:
            with open(supporting_text_path, 'r', encoding='utf-8') as file:
                supporting_content = file.read()
            print("Supporting content loaded successfully from the text file.")
        except Exception as e:
            print(f"Error reading supporting text file: {e}")
            return

    # Gather user inputs about blog details and preferences
    topic = input("Please describe what you'd like to write about: ")
    subtopics_count = int(input("Enter the number of subtopics: "))
    words_per_section = int(input("Enter the desired word count per section: "))
    blogger_identity = input("Tell me what you typically blog about, your point of view, and your intended audience: ")
    writing_style = input("Enter your preferred writing style (formal, informal, conversational): ")
    word_choice = input("Enter any specific word choice preferences (e.g., use 'use' instead of 'utilize'): ")
    print(f"Generating an outline for the topic '{topic}' with {subtopics_count} subtopics, aiming for {words_per_section} words per section.")

    # Modify the system prompt to include user preferences and language guidelines
    system_prompt = f"You are a {blogger_identity} blogger writing in a {writing_style} style. Here are the details to consider: {supporting_content} Preferred word choices: {word_choice}. Generate content accordingly."

    # Generate an outline including Introduction and Conclusion
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate a detailed blog post outline about {topic} including an Introduction, {subtopics_count} detailed subtopics, and a Conclusion. Ensure each main section and subtopic starts with '**Section' for clarity."}
        ],
        max_tokens=500  # Increased max_tokens to ensure complete responses
    )
    outline = response.choices[0].message.content.strip().split('\n')
    print("Outline generated successfully. Here's the outline:")
    print(outline)

    # Process the entire outline, capturing Introduction, each Subtopic, and Conclusion as distinct sections
    section_content = []
    current_section = []
    section_label = None  # Initialize as None to avoid capturing content before the first valid header
    for line in outline:
        if "**Section" in line or "**Introduction" in line or "**Conclusion" in line:
            if section_label is not None:  # Save current section if a label has been set
                section_content.append({"label": section_label, "content": " ".join(current_section).strip()})
            current_section = []
            section_label = line.strip().replace('**', '')  # Update section label
        if section_label is not None:
            current_section.append(line.strip())
    if section_label is not None and current_section:  # Save the last section
        section_content.append({"label": section_label, "content": " ".join(current_section).strip()})

    print("Processed sections for content generation:")
    for section in section_content:
        print(section['label'])

    # Save to CSV
    csv_filename = "blog_outline.csv"
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Section Name', 'Outline Content', 'Blog Content'])  # Define column headers

    # Generate content for each processed section and write to CSV
    contents = []
    for section in section_content:
        prompt = f"Write a detailed blog post section in the first person about the following: {section['content']} Aim for approximately {words_per_section} words."
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=int(words_per_section * 5)  # Estimating tokens based on word count
        )
        generated_content = response.choices[0].message.content.strip()
        contents.append({"section": section['label'], "content": generated_content})
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([section['label'], section['content'], generated_content])
        print(f"Generated content for {section['label']}")

    print("Blog content generated and saved to CSV.")

    # Create formatted text file
    text_filename = "blog_post.txt"
    with open(text_filename, mode='w') as file:
        for content in contents:
            file.write(content['section'] + "\n\n")  # Include section heading
            file.write(content['content'] + "\n\n")  # Include section content
    print("Blog post saved to text file.")

    return csv_filename, text_filename

# Example usage
generate_blog_post(supporting_text_path=supporting_text_path)
