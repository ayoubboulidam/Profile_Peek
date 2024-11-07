from flask import Flask, request, jsonify, render_template

from Profile_peek import ProfilePeek

# Initialize the Flask application
app = Flask(__name__)


# Route for the home page, rendering an HTML template
@app.route('/')
def home():
    return render_template('index.html')  # Serve the 'index.html' page as the homepage


# Route to handle the processing of the profile peek request, accepts only POST requests
@app.route("/process", methods=["POST"])
def process():
    # Get the 'name' parameter from the form data sent in the request
    name = request.form.get("name")

    # Check if 'name' was provided; if not, return a JSON error response with status 400
    if not name:
        return jsonify({"error": "Name is required"}), 400

    # Call the ProfilePeek function to get profile data, including a summary, profile picture URL, ice breakers, and topics of interest
    summary, profile_pic_url, ice_breakers, topics_of_interest = ProfilePeek(name=name)

    # Prepare the response by converting the summary to a dictionary format for JSON compatibility
    response = {
        "summary_and_facts": summary.to_dict(),  # Convert the summary to a dictionary
        "picture_url": profile_pic_url,  # Profile picture URL
        "ice_breakers": ice_breakers,  # List of ice breakers
        "topics_of_interest": topics_of_interest,  # List of topics of interest
    }

    # Return the response as JSON
    return jsonify(response)


# Run the application in debug mode if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)