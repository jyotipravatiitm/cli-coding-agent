import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import os
import subprocess
load_dotenv()

client = OpenAI()

def query_db(sql):
    pass

def run_command(command):
    print(f"running the tool with command : {command}")
    result = os.system(command)
    return result



def get_weather(city: str):
    # TODO!: Do an actual API Call
    print("🔨 Tool Called: get_weather", city)
    
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

def add(x, y):
    print("🔨 Tool Called: add", x, y)
    return x + y

def create_framework_project(framework, project_name):
    print("🔨 Tool Called: create_framework_project", framework, project_name)
    
    if framework not in frameworks:
        return f"Error: Framework '{framework}' not supported. Available frameworks: {', '.join(frameworks.keys())}"
    
    command = f"{frameworks[framework]} {project_name}"
    result = os.system(command)
    # Here you would typically execute the command
    # For example: os.system(command) or subprocess.run(command, shell=True)
    
    return f"Project {project_name} has been generated using {framework} framework with command: {command}"
def get_structure(project_name):
    print("🔨 Tool Called: get_strcture", project_name)
    command = f"tree -L 3 -I 'node_modules|.git|.next|dist|build|venv' {project_name}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)


    if result.returncode == 0:
            return f"Project structure for {project_name}:\n{result.stdout}"
    else:
            return f"Error running tree command: {result}"
    

def update_project(project_path, file_path, mode="list"):
    """
    Updates a project by traversing to specific folders and listing or creating files.
    
    Args:
        project_path: Base path of the project
        file_path: Path to the file/directory relative to project_path
        mode: 'list' (default) or 'create' (creates an empty file)
    
    Returns:
        String with the status of the operation
    """
    import os
    import subprocess
    
    print(f"🔨 Tool Called: update_project in {project_path}")
    
    # Combine project path with file path
    full_path = os.path.join(project_path, file_path)
    
    try:
        if mode == "list":
            # Just list the directory structure
            if os.path.exists(full_path):
                path_to_list = full_path if os.path.isdir(full_path) else os.path.dirname(full_path)
                tree_command = f"tree -L 3 -I 'node_modules|.git|.next|dist|build|venv' {path_to_list}"
                tree_output = subprocess.run(tree_command, shell=True, capture_output=True, text=True)
                tree_result = tree_output.stdout if tree_output.returncode == 0 else "Tree command failed"
                
                return f"Structure for {path_to_list}:\n{tree_result}"
            else:
                return f"Path {full_path} does not exist"
                
        elif mode == "create":
            # Ensure the directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Create an empty file if it doesn't exist
            if not os.path.exists(full_path):
                with open(full_path, 'w') as f:
                    pass  # Create empty file
                action = "created"
            else:
                action = "already exists"
                
            # Show the directory structure
            tree_command = f"tree -L 3 -I 'node_modules|.git|.next|dist|build|venv' {os.path.dirname(full_path)}"
            tree_output = subprocess.run(tree_command, shell=True, capture_output=True, text=True)
            tree_result = tree_output.stdout if tree_output.returncode == 0 else "Tree command failed"
            
            return f"File {file_path} {action} in {project_path}.\n\nUpdated structure:\n{tree_result}"
        else:
            return f"Error: Unknown mode '{mode}'"
            
    except Exception as e:
        return f"Error updating project: {str(e)}"


# This is available tools and functions
avaiable_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    },

    "create_framework_project":{
        "fn": create_framework_project,
        "description": "Takes input of the framework and creates the project"
    },
    "get_structure":{
        "fn": get_structure,
        "description": "Get structure of created project"
    },
    "update_project":{
        "fn": update_project,
        "description": "Update the project files and folders"
    }

}

frameworks = {
    # JavaScript/TypeScript frameworks
    "nextjs": "npx create-next-app",
    "react": "npx create-react-app",
    "vue": "npm install -g @vue/cli && vue create",
    "angular": "npx @angular/cli new",
    "svelte": "npx degit sveltejs/template",
    
    # Python frameworks
    "django": "django-admin startproject",
    "flask": "mkdir -p && python -m venv venv && . venv/bin/activate && pip install flask && touch",
    "fastapi": "mkdir -p && python -m venv venv && . venv/bin/activate && pip install fastapi uvicorn && touch",
    "pyramid": "pip install pyramid && pcreate -s starter",
    "django-rest": "pip install djangorestframework && django-admin startproject"
}


system_prompt = f"""
    You are an helpful AI Assistant who is specialized in resolving user queries.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution; based on the planning,
    select the relevant tool from the available tools and based on the tool selection perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for the next input.
    - Carefully analyze the user query.

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function"
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city.
    - run_command: Takes a command as input to execute on the system and returns output.
    - generate_project: Takes a project name as input and generates a project.
    - create_framework_project: Creates a project based on a given framework.
    - get_structure : Get structure of created project
    - update_project : Update the project with appropiate files and folders
    

    Example:
    User Query: Create a project
    User Query: Create a project with a specific framework

    Output: {{ "step": "action", "query": "Get info about the project the user is asking and try to suggest any specific framework if this suits the requirement. The framework can be popular react based framework or python based popular framwork" }}
    Output: {{ "step": "action", "confirmation": "Get confirmation about the project framework from user after understabnding the detailed requirement from the user. If the user wants a specific framwork, dont question more" }}
    Output: {{ "step": "action", "function": "create_framework_project", "input": "[{{\\"framework\\": \\"nextjs\\", \\"project_name\\": \\"MyNextProject\\"}}]" }}
    Output: {{ "step": "output", "content": "Provide result of the tool calling. If the tool is not available to generate a framwork based on the requirement. Apologize and suggest creating on their own" }}
    Output: {{ "step": "action", "function": "get_structure", "input":"project_name" }}
    Output: {{ "step": "plan", "content": "Confirm installer that the project is created" }}
    Output: {{ "step": "plan", "content": "Understand the structure of project and create a array of files and folders to be created for appropiate project structure" }}
    Output: {{ "step": "action", "function": "update_project", "input":"[{{\\"project_path\\": \\"my-nextjs-project\\",\\"file_path\\": \\"src/components/Button.js\\",\\"mode\\": \\"create\\"}}]" }}
    
    # Sign off with writing Readme file
"""
messages = [
    { "role": "system", "content": system_prompt }
]

while True:
    user_query = input('> ')
    messages.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        print(f" /n  LLM output {parsed_output}")
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        if parsed_output.get("step") == "plan":
            print(f'🧠: {parsed_output.get("content")}')
            continue
        
        # if parsed_output.get("step") == "action":
        #     function_name = parsed_output.get("function")
        #     tool_name = parsed_output.get("function")
        #     tool_input = parsed_output.get("input")

        #     if avaiable_tools.get(tool_name, False) != False:
        #         output = avaiable_tools[tool_name].get("fn")(tool_input) ## get the function get_weather
        #         messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
        #         continue

        if parsed_output.get("step") == "action":
            function_name = parsed_output.get("function")
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if tool_name == "update_project":
                try:
                    # Parse the input
                    if isinstance(tool_input, str):
                        parsed_input = json.loads(tool_input)
                    else:
                        parsed_input = tool_input
                    
                    # Handle both single operation and batch operations
                    if isinstance(parsed_input, list):
                        # Process multiple operations
                        results = []
                        for operation in parsed_input:
                            # Check if required fields are present for this operation
                            if not all(field in operation for field in ["project_path", "file_path"]):
                                results.append(f"Error: Missing required fields in operation: {operation}")
                                continue
                            
                            # Execute this operation
                            result = update_project(
                                operation["project_path"],
                                operation["file_path"],
                                operation.get("mode", "list")
                            )
                            results.append(result)
                        
                        # Combine all results
                        output = "\n\n".join(results)
                    else:
                        # Process single operation
                        if not all(field in parsed_input for field in ["project_path", "file_path"]):
                            output = "Error: Missing required fields. Expected: project_path, file_path"
                        else:
                            output = update_project(
                                parsed_input["project_path"],
                                parsed_input["file_path"],
                                parsed_input.get("mode", "list")
                            )
                    
                    messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                    continue
                    
                except Exception as e:
                    error_message = f"Error processing update_project input: {str(e)}"
                    messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": error_message})})
                    continue


            if avaiable_tools.get(tool_name, False) != False:
                # Parse the input which is a JSON string of an array with a single object
                try:
                    # If the input is a string representation of JSON
                    if isinstance(tool_input, str):
                        parsed_input = json.loads(tool_input)
                    else:
                        parsed_input = tool_input

                    # Handle different input formats
                    if isinstance(parsed_input, list) and len(parsed_input) > 0:
                        # If it's a list with an object inside
                        input_args = parsed_input[0]
                    elif isinstance(parsed_input, dict):
                        # If it's directly an object
                        input_args = parsed_input
                    else:
                        input_args = {}

                    # Call the function with unpacked arguments
                    output = avaiable_tools[tool_name].get("fn")(**input_args)
                    messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                    continue
                except Exception as e:
                    error_message = f"Error processing tool input: {str(e)}"
                    messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": error_message})})
                    continue
        
        if parsed_output.get("step") == "output":
            print(f'🤖: {parsed_output.get("content")}')
            break






