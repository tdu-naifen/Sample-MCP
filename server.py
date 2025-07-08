# server.py
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("Demo Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b

@mcp.tool()
def get_user_data(user_id: str) -> dict:
    """Get user data by ID."""
    # Simulated user database
    users = {
        "user1": {"name": "Alice", "age": 30, "score": 85},
        "user2": {"name": "Bob", "age": 25, "score": 92},
        "user3": {"name": "Charlie", "age": 35, "score": 78}
    }
    return users.get(user_id, {"error": "User not found"})

# === RESOURCES ===
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"

@mcp.resource("user-profile://{user_id}")
def get_user_profile(user_id: str) -> str:
    """Get formatted user profile."""
    user_data = get_user_data(user_id)
    if "error" in user_data:
        return f"User profile not found for {user_id}"
    
    return f"""
User Profile:
Name: {user_data['name']}
Age: {user_data['age']}
Score: {user_data['score']}
"""

@mcp.resource("calculation-history://{session_id}")
def get_calculation_history(session_id: str) -> str:
    """Get calculation history for a session."""
    # Simulated history
    histories = {
        "session1": ["5 + 3 = 8", "8 * 2 = 16", "16 + 10 = 26"],
        "session2": ["10 + 5 = 15", "15 * 3 = 45"],
    }
    history = histories.get(session_id, ["No history found"])
    return "\n".join(history)

# === CHAINING PROMPTS ===
@mcp.prompt()
def analyze_user_with_calculations(user_id: str, num1: str, num2: str) -> str:
    """
    Chain user data retrieval with mathematical operations.
    
    :param user_id: The user ID to analyze
    :param num1: First number for calculations
    :param num2: Second number for calculations
    :return: A prompt that chains user data with calculations
    """
    return f"""
Please perform the following chained operations:

1. First, get the user profile from resource: user-profile://{user_id}
2. Then, use the add tool to calculate: {num1} + {num2}
3. Next, use the multiply tool to calculate: {num1} * {num2}
4. Finally, create a report that includes:
   - The user's information
   - Both calculation results
   - A personalized greeting using greeting://{user_id} resource (use the user's name from step 1)

Format the final report as a comprehensive analysis.
"""

@mcp.prompt()
def mathematical_workflow(base_number: str, multiplier: str, addition: str) -> str:
    """
    Chain multiple mathematical operations in sequence.
    
    :param base_number: Starting number
    :param multiplier: Number to multiply by
    :param addition: Number to add
    :return: A prompt that chains mathematical operations
    """
    return f"""
Execute this mathematical workflow:

1. Start with the base number: {base_number}
2. Use the multiply tool to calculate: {base_number} * {multiplier}
3. Use the add tool to add {addition} to the result from step 2
4. Show each step clearly with the results
5. Provide a summary of the complete workflow

Please execute each step in sequence and show your work.
"""

@mcp.prompt()
def user_score_analysis(user_id: str) -> str:
    """
    Analyze user performance with calculations and resources.
    
    :param user_id: The user ID to analyze
    :return: A prompt that combines user data with score calculations
    """
    return f"""
Perform a comprehensive user score analysis:

1. Get user data using the get_user_data tool for user: {user_id}
2. Access the user profile resource: user-profile://{user_id}
3. If the user has a score, calculate bonus points:
   - Use the multiply tool: score * 2 (for double points)
   - Use the add tool: original_score + bonus_points
4. Get a personalized greeting using greeting://[user_name] resource
5. Create a final report including:
   - User information
   - Original score
   - Bonus calculation
   - Final score
   - Personalized greeting

Present this as a complete performance analysis.
"""

@mcp.prompt()
def session_report(session_id: str, user_id: str) -> str:
    """
    Generate a comprehensive session report combining history and user data.
    
    :param session_id: The session ID
    :param user_id: The user ID
    :return: A prompt that chains session history with user analysis
    """
    return f"""
Generate a comprehensive session report:

1. Get calculation history from resource: calculation-history://{session_id}
2. Get user profile from resource: user-profile://{user_id}
3. Use get_user_data tool to get detailed user information for {user_id}
4. Count the number of calculations in the history (use tools if needed)
5. Get a greeting using greeting://[user_name] resource
6. Create a final report containing:
   - Session summary
   - User information
   - Calculation history
   - Statistics about the session
   - Personalized conclusion

Format as a professional session report.
"""

# Original prompt
@mcp.prompt()
def review_code(code: str) -> str:
    """
    Provide a template for reviewing code.

    :param code: The code to review.
    :return: A prompt that asks the LLM to review the code.
    """
    return f"Please review this code:\n\n{code}"

if __name__ == "__main__":
    mcp.run()