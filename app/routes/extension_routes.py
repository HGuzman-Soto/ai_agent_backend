from flask import Blueprint, session, redirect, url_for, request, jsonify

bp = Blueprint('extension', __name__, url_prefix='/extension')


# In-memory list to store URLs (for now)
saved_urls = []

# Route to recieve urls from backend
@bp.route('/store_urls', methods=['POST'])
def store_urls():
    data = request.get_json()
    print("Data received:", data)
    saved_urls = data.get('urls', [])
    print("Urls received:", saved_urls)
    return jsonify({
        'message': 'URLs received and saved successfully',
        'urls': saved_urls
    })



# def receive_urls():
#     data = request.get_json()
#     print("Data received:", data)
#     urls = data.get('urls', [])

#     print("URLs received:", urls)  # Debug
#     # Append only unique URLs to the saved_urls list
#     for url in urls:
#         if not any(saved_url['url'] == url['url'] for saved_url in saved_urls):
#             saved_urls.append(url)

#     print("Current saved URLs:", saved_urls)  # Debugging purposes

#     # Return a success message
#     return jsonify({
#         'message': 'URLs received and saved successfully',
#         'urls': urls
    # })