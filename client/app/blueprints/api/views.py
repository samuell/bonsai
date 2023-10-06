"""Declaration of flask api entrypoints"""
from flask import Blueprint, request, session, jsonify, flash
from flask_login import login_required, current_user
from app.bonsai import add_samples_to_basket, remove_samples_from_basket, TokenObject
from app.models import SampleBasketObject
import json


api_bp = Blueprint("api", __name__, template_folder="templates", static_folder="static")


@api_bp.route("/api/basket/add", methods=["POST"])
@login_required
def add_sample_to_basket():
    """Add sample to basket."""
    # if not valid token
    if current_user.get_id() is None:
        return jsonify("Not authenticated"), 401

    # add samples to basket
    raw_samples = json.loads(request.data).get("selectedSamples")
    # cast to correct type
    samples_to_add = [SampleBasketObject(**smp) for smp in raw_samples]
    try:
        token = TokenObject(**current_user.get_id())
        add_samples_to_basket(token, samples=samples_to_add)
    except Exception as error:
        flash(str(error), "warning")
        return "Error", 500
    else:
        return "Added", 200


@api_bp.route("/api/basket/remove", methods=["POST"])
@login_required
def remove_sample_from_basket():
    """Remove sample from basket."""
    # if not valid token
    if current_user.get_id() is None:
        return "Not authenticated", 401

    # verify input
    request_data = json.loads(request.data)
    sample_id = request_data.get("sample_id", None)
    remove_all = request_data.get("remove_all", False)
    if sample_id is None and not remove_all:
        return "Invalid input", 500

    token = TokenObject(**current_user.get_id())
    if remove_all:
        to_remove = [sample["sample_id"] for sample in current_user.basket]
    else:
        to_remove = [sample_id]
    # call bonsai api to remove samples from basket
    remove_samples_from_basket(token, sample_ids=to_remove)

    return f"removed {len(to_remove)}", 200
