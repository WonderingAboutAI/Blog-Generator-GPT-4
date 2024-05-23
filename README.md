# Blog-Generator-GPT-4
This Python script is intended to combat model "laziness" by prompting OpenAI's GPT-4 to generate an outline and then feeding it the outline one section at a time for copywriting.

**You will need an OpenAI API key to run this script.** 

## Features

### Prompt Development
Allows users to define the blog's topic, number of subtopics, word count per section, blogging identity, writing style, and specific word preferences to shape the content's tone and complexity.

### Phased Content Generation
Automatically generates a structured outline with clearly labeled sections. These sections are used as inputs for generating the blog. GPT-4 is promoted to generate copy for each section of the outline and achieve the desired word count.

### Support for Lengthy Instructions 
Incorporates additional insights, examples, and/or style guidelines provided through a supporting text file, enhancing the relevancy and depth of the generated content.

### Output Management
Outputs the blog post section titles, outline content, and blog content into a CSV file with three columns labaled Section Name, Outline Content, and Blog Content. Outputs the blog copy into a text file.

## Usage

To run the script:

1. Ensure that Python and necessary packages are installed.
2. Set up your .env file with your OPENAI_API_KEY.
3. Define the path to your supporting text file directly in the script or modify the script to accept it as a command-line argument.
4. Execute the script and follow the on-screen prompts to input your blog post details.
5. Open outputs **blog_outline.csv and blog_post.txt.**
