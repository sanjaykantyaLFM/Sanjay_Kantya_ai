def calculator(expression):

    try:
        result = eval(expression)   # eval() func it take string in it and execute as python code and perform operation autamatically
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"
    

    # imp function here is **eval()***