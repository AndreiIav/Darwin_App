from flask import Blueprint, current_app, jsonify, request

# Blueprint Configuration
log_bp = Blueprint("log_bp", __name__)


@log_bp.route("/log/log_click_magazine_link", methods=["POST"])
def log_magazine_link_click():
    data = request.json
    link = data.get("link")

    current_app.logger.info(f"Clicking on magazine link: {link}")

    return jsonify(success=True)
