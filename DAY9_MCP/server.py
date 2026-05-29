from mcp.server.fastmcp import FastMCP

#create mcp 
mcp = FastMCP("My First MCP Server")

#learnign demo part

#create tool
# @mcp.tool()      # this is for Tool registration  without it the below func is normal python function 
# def greet(name: str) -> str:
#     """
#     Greet a user.
#     """ 
#     return f"Hello, {name}! Welcome to mcp."



# calculator part

@mcp.tool() # this is for Tool registration  without it the below func is normal python function 
def add(a: int, b: int) -> int:
    """
    
    Adds two integer numbers and returns the result.
    Use this tool whenever a mathematical addition operation is required.
    """
    return a+b

@mcp.tool()
def subtract(a:int, b:int):
    """
    Subtract two integer numbers and returns the result.

    Use this tool whenever a mathematical subtraction operation is required.

    """
    return a-b

@mcp.tool()
def multiply(a:int, b:int):
    """
    Multiply two integer numbers and returns the result.
    Use this tool whenever a mathematical multiplication operation is required.
    """
    return a*b

@mcp.tool()
def divide(a:int, b:int) -> float:
    """

    divide two integer numbers and returns the result.
    Use this tool whenever a mathematical division operation is required.
    """

    if b == 0:
        raise ValueError("Division by zero is not allowed")
    
    return a/b




# now the reader file part
@mcp.tool()
def read_file(file_path: str) -> str:
    """
    Reads the contents of a text file and returns the text.

    Use this tool when file data needs to be accessed or analyzed.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
        
    except FileNotFoundError:
        return "Error : File not found"
    
    except Exception as e:
        return f"Error: {str(e)}"



# word counter 
@mcp.tool()
def count_words(text: str) -> int:
    """
    Count the number of words in a text.
    """

    return len(text.split())


# it tell about my project

@mcp.resource("info://project")
def project_info() -> str:
    """
    Provides information about this MCP learning project.
    """
    return """
    MCP Learning Project

    Available Tools:
    - add
    - subtract
    - multiply
    - divide
    - read_file
    - count_words

    Built using Python MCP SDK.
    """

# this is exxamples to know about this project details and summarize
@mcp.prompt()
def summarize_text(text: str) -> str:
    """
    Creates a prompt for summarizing text.
    """
    return f"""
    Summarize the following text in simple language:

    {text}
    """
#run server 
if __name__ == "__main__":
    mcp.run()

