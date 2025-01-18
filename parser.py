from lark import Lark, Tree, Token
output_dir = "outdir"
grammar = """
    start: function+
    function: "fn" CNAME "{" statement* "}"
    execute_as: "execute as" entity "{" statement* "}"    
    entity: CNAME
    statement: int_declaration | while_loop | intvar_int_add | functioncall | execute_as 
    functioncall: CNAME"(" argument* ")"  -> func_call
            | CNAME"(" ")" -> func_call
    argument: CNAME
    int_declaration: "int" CNAME "=" NUMBER
    while_loop: "while" condition "{" statement* "}"
    intvar_int_add: CNAME "+=" NUMBER
    condition: CNAME "<=" NUMBER

    %import common.CNAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar)

# Source code
source_code = """
fn main {
    int count = 0
    count += 1
    main(count)
    execute as someone {
        print(something) 
    }
}
"""
# Traverse the tree
isfunctiondecl = False
isintdecl = False
funcfile = None
isintvar_int_add = False
current_var = None
intvar_int_addoperands = None
funcnames = []
builtinfuncs = ["print", "summon"]
varstore = {}

"""def traverse_tree(node):
    global isfunctiondecl, isvardecl, funcfile, current_var

    if isinstance(node, Tree):
        print(f"Tree: {node.data}")
        if node.data == "function":
            isfunctiondecl = True
        if node.data == "int_declaration":
            isintdecl = True
            current_var = {}  # Start a new variable
        if node.data == "intvar_int_add":
            isintvar_int_add = True
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

        if isintdecl:
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
                varstore[current_var.get("name")] = currentvar.get("value")
                isvardecl = False  # Done with this variable
                current_var = None  # Reset for the next variable
        if isintvar_int_add:
            if node.type == "CNAME":
                intvar_int_addoperands["var"] = node.value
            elif node.type == "NUMBER":
                current_var["int"] = node.value
            if "var" in intvar_int_addoperands and "int" in intvar_int_addoperands:
                if funcfile:
                    with open(funcfile, "a") as f:
                        cmdwrite = "function defaults:intvar_int_add {x:" + intvar_int_addoperands.get("var") + ",y:" + intvar_int_addoperands.get("int") + "}"
                        f.write("function defaults:intvar_int_add {\n")
                else:
                    print("Error: Function file not set.")
                varstore[current_var.get("name")] = currentvar.get("value")
                isvardecl = False  # Done with this variable
                current_var = None  # Reset for the next variable
"""
def tokenize(node):
    if isinstance(node, Tree):
        print(f"Tree: {node.data}")
        for child in node.children:
            tokenize(child)
    elif isinstance(node,Token):
        print(f"Token: {node.type} -> {node.value}")
# Parse and traverse
def parsefile(source_code):
    tree = parser.parse(source_code)
    traverse_tree(tree)
tree = parser.parse(source_code)
tokenize(tree)