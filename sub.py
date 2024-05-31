import subprocess
import os
from github import Github
from git import Repo

# LeetCode credentials and settings
leetcode_username = "BechirKefi12"
leetcode_password = "LeetCodeBechir@20"
problem_slug = "two-sum"  # example problem slug

# GitHub credentials and settings
github_token = "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"
repo_name = "leetcode"
repo_url = f"https://github.com/bechir105/leetcode.git"

# Directory for your solutions
solutions_dir = "solutions"

# Step 1: Log in to LeetCode
def leetcode_login():
    subprocess.run(["leetcode", "user", "-l", leetcode_username, leetcode_password], check=True)

# Step 2: Fetch the problem and generate the solution file
def fetch_problem(problem_slug):
    subprocess.run(["leetcode", "show", problem_slug, "-gx"], check=True)

# Step 3: Solve the problem (Here, we assume you manually solve it or use an existing solution)
# Save your solution to a file named after the problem slug
def save_solution(problem_slug, solution_code):
    with open(os.path.join(solutions_dir, f"{problem_slug}.py"), "w") as file:
        file.write(solution_code)

# Step 4: Push the solution to GitHub
def push_to_github(problem_slug):
    # Initialize the repo object
    repo = Repo(solutions_dir)
    
    # Add the new solution file
    repo.index.add([f"{problem_slug}.py"])
    
    # Commit the changes
    repo.index.commit(f"Add solution for {problem_slug}")
    
    # Push to GitHub
    origin = repo.remote(name='origin')
    origin.push()

# Main function to orchestrate the steps
def main():
    # Log in to LeetCode
    leetcode_login()
    
    # Fetch the problem
    fetch_problem(problem_slug)
    
    # Solve the problem and save the solution (You can customize this part)
    solution_code = """
# Your solution code here
class Solution:
    def twoSum(self, nums, target):
        hash_map = {}
        for i, num in enumerate(nums):
            if target - num in hash_map:
                return [hash_map[target - num], i]
            hash_map[num] = i
    """
    save_solution(problem_slug, solution_code)
    
    # Push the solution to GitHub
    push_to_github(problem_slug)

if __name__ == "__main__":
    main()
