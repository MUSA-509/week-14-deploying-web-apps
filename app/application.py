"""Musa 509 week 14 demo app"""
import json

from flask import Flask, request, render_template, Response
import requests

try:
    from geopy import distance
except ImportError:
    pass

MEYERSON_LAT = 39.9522197
MEYERSON_LNG = -75.1927961

# mapbox
with open("./secrets/mapbox_token.json", "r") as mb_token:
    MAPBOX_TOKEN = json.load(mb_token)["token"]

application = Flask(__name__, template_folder="templates")


@application.route("/")
def index():
    """User input page"""
    return Response(render_template("index.html"), 200, mimetype="text/html")


def get_address(args):
    """Parses query strings"""
    text_address = args.get("address_text")
    dropdown_address = args.get("address_dropdown")
    if text_address == "" and dropdown_address != "":
        return dropdown_address
    if text_address != "":
        return text_address
    return False


def distance_from_meyerson(lng, lat):
    """Calculates the distance from Meyerson Hall"""
    return round(distance.distance((MEYERSON_LAT, MEYERSON_LNG), (lat, lng)).km, 2)


@application.route("/whereami")
def whereami():
    """Landing page"""
    address = get_address(request.args)
    error_message = None

    if address is not None:
        geocoding_call = (
            f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json"
        )
        resp = requests.get(geocoding_call, params={"access_token": MAPBOX_TOKEN})

        # BUGFIX
        # COMMENT OUT THE FOLLOWING LINE
        lng, lat = resp.json()["features"][0]["geometry"]["coordinates"]

        # UNCOMMENT THE FOLLOWING EIGHT LINES
        # if "features" in resp.json():
        #     lng, lat = resp.json()["features"][0]["geometry"]["coordinates"]
        # else:
        #     error_message = (
        #         f"Invalid address entered ({address}). Here's Meyerson Hall."
        #     )
        #     lat, lng = MEYERSON_LAT, MEYERSON_LNG
        #     address = "Meyerson Hall, University of Pennsylvania"
    else:
        lat, lng = MEYERSON_LAT, MEYERSON_LNG
        address = "No address entered"

    return render_template(
        "whereami.html",
        error_message=error_message,
        address=address,
        # UNCOMMENT the following line for Prompt #2
        # distance_meyerson=distance_from_meyerson(lng, lat),
        lat=lat,
        lng=lng,
        html_map=render_template(
            "point_map.html", lat=lat, lng=lng, mapbox_token=MAPBOX_TOKEN
        ),
    )


# 404 page example
@application.errorhandler(404)
def page_not_found(err):
    """404 page"""
    return f"404 ({err})"


if __name__ == "__main__":
    application.jinja_env.auto_reload = True
    application.config["TEMPLATES_AUTO_RELOAD"] = True
    application.run(debug=True)
