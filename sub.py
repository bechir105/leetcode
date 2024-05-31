import os
import json
import subprocess

# Define the path to the local JSON file containing problem data
problems_json_file = "problems_test.json"

# Ensure solutions and outputs directories exist
solutions_dir = "solutions"
outputs_dir = "outputs"
os.makedirs(solutions_dir, exist_ok=True)
os.makedirs(outputs_dir, exist_ok=True)

# Step 1: Load problems from JSON file
def load_problems_from_json(json_file):
    with open(json_file, "r") as file:
        problems = json.load(file)
    return problems

# Step 2: Save the solution code to a Python file, adding necessary imports
def save_solution(problem_slug, solution_code):
    file_path = os.path.join(solutions_dir, f"{problem_slug}.py")
    with open(file_path, "w") as file:
        file.write("from typing import List\n" + solution_code)
    return file_path

# Step 3: Execute the solution code and capture the output
def execute_solution(solution_file, test_case_code):
    with open(solution_file, "a") as file:
        file.write("\n\n" + test_case_code)

    command = f"python {solution_file}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    return stdout, stderr

# Step 4: Save the output to a file
def save_output(problem_slug, output):
    with open(os.path.join(outputs_dir, f"{problem_slug}_output.txt"), "w") as file:
        file.write(output)

# Generate test case code from the problem metadata
def generate_test_case_code(metadata):
    function_name = metadata["function_name"]
    parameters = metadata["parameters"]
    example_input = metadata["example_input"]
    
    # Prepare the input arguments as string
    input_args = ", ".join([f"{k}={repr(v)}" for k, v in example_input.items()])
    
    test_case_code = f"""
if __name__ == "__main__":
    solution = Solution()
    print(solution.{function_name}({input_args}))
"""
    return test_case_code

# Main function to orchestrate the steps
def main():
    try:
        # Step 1: Load problems from JSON file
        problems = load_problems_from_json(problems_json_file)
        
        for problem in problems:
            problem_title = problem["title"]
            
            # Create a slug for the file name from the problem title
            problem_slug = problem_title.lower().replace(" ", "-")
            
            # Step 2: Save the solution to a file
            solution_code = problem["openai_response"]
            solution_file = save_solution(problem_slug, solution_code)
            
            # Step 3: Generate the test case code
            metadata = problem["metadata"]
            test_case_code = generate_test_case_code(metadata)
            
            # Step 4: Execute the solution code and capture the output
            stdout, stderr = execute_solution(solution_file, test_case_code)
            
            if stderr:
                raise Exception(f"Error while executing solution for {problem_title}: {stderr}")
            
            # Step 5: Save the output to a file
            save_output(problem_slug, stdout)
            
            print(f"Solution and output files generated successfully for {problem_title}.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
