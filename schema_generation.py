from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json
import copy


    



def prepare_valid_output_schema(schema: dict) -> dict:
    """
    Returns a new schema with updates such that the schema:
    1) has 'required' = list of all its properties
    2) has 'additionalProperties' = false
    3) has a key "schema" that has an object at the top level
    4) has a key "name" that is a valid name according to the pattern ^[a-zA-Z0-9_-]+$
    5) has all $defs at the top level
    """
    # Make a deep copy to avoid altering the original schema
    new_schema = copy.deepcopy(schema)

    def process_schema(node: dict) -> dict:
        if node.get("type") == "object" and "properties" in node:
            # Set 'required' to list all keys in 'properties'
            node["required"] = list(node["properties"].keys())
            # Disallow additional properties
            node["additionalProperties"] = False

        # Recurse into sub-properties
        if "properties" in node and isinstance(node["properties"], dict):
            node["properties"] = {
                key: process_schema(sub_node)
                for key, sub_node in node["properties"].items()
            }

        # Recurse into array items if type is 'array'
        if node.get("type") == "array" and "items" in node:
            items = node["items"]
            if isinstance(items, dict):
                node["items"] = process_schema(items)
            elif isinstance(items, list):
                node["items"] = [process_schema(item) for item in items]

        return node
    new_schema = process_schema(new_schema)


    full_schema = {}
    
    schema_defs = None
    name = None
    
    # get name of the schema
    if "name" in new_schema and "type" in new_schema:
        name = new_schema["name"]
        del new_schema["name"]
    elif "name" in new_schema and "schema" in new_schema:
        name = new_schema["name"]

    # extract defs
    if "$defs" in new_schema:
        schema_defs = new_schema["$defs"]
        del new_schema["$defs"]

    if "schema" in new_schema:
        new_schema = new_schema["schema"]
    
    
    # convert array schema to object schema with items key
    if "type" in new_schema and new_schema["type"] == "array":
        s = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": new_schema
                } 
            },
            "required": ["items"],
            "additionalProperties": False
        }
        new_schema = s
    
    # Ensure schema name matches pattern ^[a-zA-Z0-9_-]+$ by replacing whitespace with underscore
    # and removing any other invalid characters
    full_schema["name"] = "".join(c if c.isalnum() or c in "_-" else "_" if c.isspace() else "" for c in name)
    full_schema["schema"] = new_schema

    # add defs if they exist
    if schema_defs:
        full_schema["$defs"] = schema_defs

   
    return full_schema

def generate_schema(messages: list[str]):

    print(messages)

    with open("meta_schema.json", "r") as file:
       meta_schema = json.load(file)

    with open("system_prompt.txt", "r") as file:
        system_prompt_content = file.read()

    

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    llm_with_structured_output = llm.with_structured_output(meta_schema, method="json_schema")

    result = llm_with_structured_output.invoke([SystemMessage(content=system_prompt_content), *messages])
    print("result after invoke")
    print(result)
    result = prepare_valid_output_schema(result)
    print("result after prepare_valid_output_schema")
    print(result)

    return result