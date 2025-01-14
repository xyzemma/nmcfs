from lark import Lark, Tree, Token
output_dir = "outdir"
# Updated grammar
grammar = """
    start: function+
    function: "fn" CNAME "{" statement* "}"
    statement: var_declaration | while_loop | varintadd | functioncall
    functioncall: CNAME"(" argument* ")"
    argument: CNAME
    var_declaration: "int" CNAME "=" NUMBER
    while_loop: "while" condition "{" statement* "}"
    varintadd: CNAME "+=" NUMBER
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
}
"""
# Traverse the tree
isfunctiondecl = False
isvardecl = False
funcfile = None
isvarintadd = False
current_var = None
varintaddoperands = None
funcnames = []
varstore = {}

def traverse_tree(node):
    global isfunctiondecl, isvardecl, funcfile, current_var

    if isinstance(node, Tree):
        print(f"Tree: {node.data}")
        if node.data == "function":
            isfunctiondecl = True
        if node.data == "var_declaration":
            isvardecl = True
            current_var = {}  # Start a new variable
        if node.data == "varintadd":
            isvarintadd = True
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
                varstore[current_var.get("name")] = currentvar.get("value")
                isvardecl = False  # Done with this variable
                current_var = None  # Reset for the next variable
        if isvarintadd:
            if node.type == "CNAME":
                varintaddoperands["var"] = node.value
            elif node.type == "NUMBER":
                current_var["int"] = node.value
            if "var" in varintaddoperands and "int" in varintaddoperands:
                if funcfile:
                    with open(funcfile, "a") as f:
                        cmdwrite = "function defaults:varintadd {x:" + varintaddoperands.get("var") + ",y:" + varintaddoperands.get("int") + "}"
                        f.write("function defaults:varintadd {\n")
                else:
                    print("Error: Function file not set.")
                varstore[current_var.get("name")] = currentvar.get("value")
                isvardecl = False  # Done with this variable
                current_var = None  # Reset for the next variable

# Parse and traverse
def parsefile(source_code):
    tree = parser.parse(source_code)
    traverse_tree(tree)