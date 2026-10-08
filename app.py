from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)


def generate_documentation(code):
    """
    Analyze Flask API code and generate basic API documentation.
    """

    endpoints = []

    # Find Flask routes
    pattern = r'@app\.route\(["\'](.*?)["\'](?:,\s*methods=\[(.*?)\])?\]'

    matches = re.findall(pattern, code)

    for route, methods in matches:

        # Default method
        if methods:
            method_list = re.findall(r'["\'](.*?)["\']', methods)
        else:
            method_list = ["GET"]

        # Find function after the route
        route_position = code.find(f'@app.route')
        remaining_code = code[route_position:]

        function_match = re.search(
            r'def\s+(\w+)\s*\(',
            remaining_code
        )

        function_name = (
            function_match.group(1)
            if function_match
            else "API Function"
        )

        for method in method_list:

            endpoints.append({
                "method": method.upper(),
                "route": route,
                "function": function_name,
                "description": create_description(
                    method.upper(),
                    route,
                    function_name
                )
            })

    return endpoints


def create_description(method, route, function):

    if "get" in function.lower():
        return "Retrieve data from the API."

    if "create" in function.lower() or "post" in function.lower():
        return "Create new data using the API."

    if "update" in function.lower() or "put" in function.lower():
        return "Update existing data using the API."

    if "delete" in function.lower():
        return "Delete data using the API."

    if method == "GET":
        return "Retrieve information from the API."

    if method == "POST":
        return "Create new information using the API."

    if method == "PUT":
        return "Update existing information using the API."

    if method == "DELETE":
        return "Delete information using the API."

    return "API endpoint."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()

    code = data.get("code", "")

    if not code.strip():
        return jsonify({
            "success": False,
            "message": "Please enter API code."
        })

    documentation = generate_documentation(code)

    return jsonify({
        "success": True,
        "documentation": documentation
    })


if __name__ == "__main__":
    app.run(debug=True)