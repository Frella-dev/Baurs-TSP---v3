from urllib.parse import quote


GOOGLE_MAPS_BASE = (
    "https://www.google.com/maps/dir/?api=1"
)


def coordinate_string(
    lat,
    lon
):

    return f"{lat},{lon}"


def build_google_maps_url(
    day,
    office_lat=None,
    office_lon=None
):

    if len(day) == 0:

        return None

    if len(day) == 1:

        destination = coordinate_string(
            day[0]["Latitude"],
            day[0]["Longitude"]
        )

        return (
            "https://www.google.com/maps/search/?api=1"
            f"&query={destination}"
        )

    origin = coordinate_string(
        day[0]["Latitude"],
        day[0]["Longitude"]
    )

    destination = coordinate_string(
        day[-1]["Latitude"],
        day[-1]["Longitude"]
    )

    waypoints = []

    for stop in day[1:-1]:

        waypoints.append(
            coordinate_string(
                stop["Latitude"],
                stop["Longitude"]
            )
        )

    waypoint_string = "|".join(
        waypoints[:23]
    )

    return (
        f"{GOOGLE_MAPS_BASE}"
        f"&origin={origin}"
        f"&destination={destination}"
        f"&travelmode=driving"
        f"&waypoints={quote(waypoint_string)}"
    )


def build_day_route_url(
    day,
    office_lat=None,
    office_lon=None
):

    return build_google_maps_url(
        day,
        office_lat,
        office_lon
    )


def build_area_route_url(
    customers,
    office_lat=None,
    office_lon=None
):

    return build_google_maps_url(
        customers,
        office_lat,
        office_lon
    )


def build_single_customer_url(
    customer,
    office_lat=None,
    office_lon=None
):

    destination = coordinate_string(
        customer["Latitude"],
        customer["Longitude"]
    )

    return (
        "https://www.google.com/maps/search/?api=1"
        f"&query={destination}"
    )
