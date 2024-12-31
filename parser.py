from lark import Tree, Token

# Global state
output_dir = "./output"
isfunctiondecl = False
isvardecl = False
funcfile = None
current_var = None  # To hold the variable being processed

def traverse_tree(node):
    global isfunctiondecl, isvardecl, funcfile, current_var

    if isinstance(node, Tree):
        print(f"Tree: {node.data}")
        if node.data == "function":
            isfunctiondecl = True
        if node.data == "var_declaration":
            isvardecl = True
            current_var = {}  # Start a new variable
        for child in node.children:
            traverse_tree(child)

    elif isinstance(node, Token):
        print(f"Token: {node.type} -> {node.value}")

        if isfunctiondecl:
            funcname = node.value
            funcfile = f"{output_dir}/{funcname}.mcfunction"
            # Initialize the function file
            with open(funcfile, "w") as f:
                f.write(f"# Function {funcname}\n")
            isfunctiondecl = False

        if isvardecl:
            if node.type == "CNAME":
                current_var["name"] = node.value
            elif node.type == "NUMBER":
                current_var["value"] = node.value

            # Check if the variable is fully defined
            if "name" in current_var and "value" in current_var:
                if funcfile:
                    with open(funcfile, "a") as f:
                        f.write(f"data modify storage variables {current_var['name']} set value {current_var['value']}\n")
                else:
                    print("Error: Function file not set.")
                isvardecl = False  # Done with this variable
                current_var = None  # Reset for the next variable
