from lark import Lark, Tree, Token
import os
output_dir = "outdir"
grammar = """
    start: namespace+
    namespace: "namespace" CNAME "{" function+ "}"
    function: "fn" CNAME "{" statement* "}"
    execute_as: "execute as" entity "{" statement* "}"    
    entity: CNAME
    statement: var_declaration | while_loop | var_operation | functioncall | execute_as 
    functioncall: CNAME"(" argument* ")"  -> func_call
    argument: vararg | numarg | stringarg | methodarg | operationarg
    vararg: CNAME
    stringarg: ESCAPED_STRING
    numarg: NUMBER
    methodarg: functioncall
    operationarg: var_operation
    var_declaration: type CNAME "=" NUMBER
    type: int | float | bool | array | string
    int: "int"
    float: "float"
    bool: "bool"
    array: "array"
    string: "string"
    while_loop: "while" condition "{" statement* "}"
    var_operation: operand operator operand
    operand: NUMBER | CNAME
    operator: add | subtract | divide | multiply
    add: "+=" | "+"
    subtract: "-=" | "+"
    divide: "/=" | "/"
    multiply: "*=" | "*"
    condition: CNAME "<=" NUMBER

    %import common.ESCAPED_STRING
    %import common.CNAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar)

# Source code
source_code = """
namespace main{
    fn main {
        int count = 0
        count += 1
        main(count)
        execute as someone {
            print("Hello World")
            print(count)
            print(3+3) 
        }
    }
}
"""

isfunctiondecl = False
isvardecl = False
funcfile = None
isoperation = False
current_var = None
operands = None
isnamespaceinit = False
namespace = None
funcnames = []
builtinfuncs = ["print", "summon"]
varstore = {}

def dpinit():
    with open(f"{output_dir}/pack.mcmeta","w+") as packmcmeta:
        packmcmeta.write("""{
  "pack": {
    "description": "Generated with nmcfs",
    "pack_format": 61
  }
}""")
def traverse_tree(node):
    global isfunctiondecl, isvardecl, funcfile, current_var, isoperation, isnamespaceinit, namespace, funcfile

    if isinstance(node, Tree):
        print(f"Tree: {node.data}")
        if node.data == "start":
            dpinit()
        if node.data == "namespace":
            isnamespaceinit = True
        if node.data == "function":
            isfunctiondecl = True
        if node.data == "int_declaration":
            isintdecl = True
            current_var = {}
        if node.data == "intvar_int_add":
            isintvar_int_add = True
        for child in node.children:
            traverse_tree(child)

    elif isinstance(node, Token):
        print(f"Token: {node.type} -> {node.value}")

        if isfunctiondecl:
            funcname = node.value
            os.makedirs(f"{output_dir}/data/{namespace}/function")
            funcfile = f"{output_dir}/data/{namespace}/function/{funcname}.mcfunction"
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
        if isoperation:
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
        if isnamespaceinit:
            namespace = node.value
            isnamespaceinit = False

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
#tokenize(tree)
traverse_tree(tree)