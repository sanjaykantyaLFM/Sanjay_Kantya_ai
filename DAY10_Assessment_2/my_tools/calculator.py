from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression and return the result.
    Example: 25*12, 100+50, 20/4
    """

    try:
        result = eval(expression)
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"