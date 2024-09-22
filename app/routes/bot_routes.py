from flask import Blueprint, request, jsonify
from app.services import agent

bp = Blueprint('bot', __name__, url_prefix='/bot')


@bp.route('/query', methods=['GET'])
def run_bot():
    print('calling run_bot')
    '''Api route to call bot

    Args:
        user_id (str): user id
    
    Returns:
        dict: problems for user if successfuly, else error message
    '''

    urls = [
            "https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf",
            "https://research.facebook.com/publications/flexiraft-flexible-quorums-with-raft/",
            "https://www.foundationdb.org/files/fdb-paper.pdf"
    ]


    response = []
    # Process the URLs and print the results
    results = agent.process_urls(urls)
    for i, result in enumerate(results):
        print(f"Thoughts on {urls[i]}:\n{result}\n")
        response.append(f"Thoughts on {urls[i]}:\n{result}\n")
    return jsonify(response)



