# cli-coding-agent
This project helps to create project like Claude Code CLI. You need to have OpenAI key to create the project
CLI Framework Project Generator
A command-line tool that leverages LLMs to create and update projects based on various frameworks. This agent-based CLI tool can generate projects, manage project structures, and create files - all through natural language interactions.

Features
Create projects using popular frameworks (React, Next.js, Django, Flask, etc.)
View project structures with intelligent filtering (excluding large directories like node_modules)
Update project structures by adding new files and directories
Batch operations for creating multiple files at once
LLM-powered assistance for project structure recommendations
Supported Frameworks
JavaScript/TypeScript Frameworks
Next.js
React
Vue
Angular
Svelte
Python Frameworks
Django
Flask
FastAPI
Pyramid
Django REST Framework
Installation
Prerequisites
Python 3.8+
Node.js and npm (for JavaScript frameworks)
Git
Setup
Clone the repository:
bash
git clone <repository-url>
cd cli-agent
Create a virtual environment:
bash
python -m venv venv
Activate the virtual environment:
On Windows:
bash
venv\Scripts\activate
On macOS/Linux:
bash
source venv/bin/activate
Install the required dependencies:
bash
pip install -r requirements.txt
Create a .env file with your OpenAI API key:
OPENAI_API_KEY=your_api_key_here
Usage
Run the agent:

bash
python agent.py
Example Commands
You can interact with the agent using natural language:

> Create a Next.js project called my-portfolio
> Create a Flask API for a todo app
> Update my-portfolio project with component files
How It Works
The agent parses your natural language query
It plans the necessary steps using an LLM
It selects and calls appropriate tools to perform actions
It observes the results and provides feedback
It can continue with additional actions based on the current state
Project Structure
cli-agent/
├── agent.py          # Main agent implementation
├── requirements.txt  # Python dependencies
└── README.md         # This file
Requirements
Create a requirements.txt file with the following contents:

openai
python-dotenv
requests
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

License
This project is licensed under the MIT License - see the LICENSE file for details.

