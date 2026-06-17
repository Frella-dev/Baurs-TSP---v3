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
    office_lat,
    office_lon
):
    """
    Google Maps route link

    Google waypoint limit:
    approximately 23 waypoints

    For larger routes we truncate.
    """

    if len(day) == 0:

        return None

    origin = coordinate_string(
        office_lat,
        office_lon
    )

    destination = coordinate_string(
        day[-1]["Latitude"],
        day[-1]["Longitude"]
    )

    waypoints = []

    for stop in day[:-1]:

        waypoints.append(
            coordinate_string(
                stop["Latitude"],
                stop["Longitude"]
            )
        )

    waypoint_string = "|".join(
        waypoints[:23]
    )

    url = (
        f"{GOOGLE_MAPS_BASE}"
        f"&origin={origin}"
        f"&destination={destination}"
        f"&travelmode=driving"
        f"&waypoints={quote(waypoint_string)}"
    )

    return url


def build_day_route_url(
    day,
    office_lat,
    office_lon
):

    return build_google_maps_url(
        day,
        office_lat,
        office_lon
    )


def build_area_route_url(
    customers,
    office_lat,
    office_lon
):

    return build_google_maps_url(
        customers,
        office_lat,
        office_lon
    )


def build_single_customer_url(
    customer,
    office_lat,
    office_lon
):

    origin = coordinate_string(
        office_lat,
        office_lon
    )

    destination = coordinate_string(
        customer["Latitude"],
        customer["Longitude"]
    )

    return (
        f"{GOOGLE_MAPS_BASE}"
        f"&origin={origin}"
        f"&destination={destination}"
        f"&travelmode=driving"
    )


def build_customer_search_url(
    customer_name,
    town=None
):

    query = customer_name

    if town:

        query = (
            f"{customer_name} "
            f"{town}"
        )

    query = quote(query)

    return (
        "https://www.google.com/maps/search/?api=1"
        f"&query={query}"
    )


def get_route_statistics(
    day
):

    if len(day) == 0:

        return {
            "stops": 0,
            "first_stop": None,
            "last_stop": None
        }

    return {
        "stops": len(day),
        "first_stop":
            day[0].get(
                "Customer name"
            ),
        "last_stop":
            day[-1].get(
                "Customer name"
            )
    }


def build_navigation_links(
    days,
    office_lat,
    office_lon
):

    result = []

    for idx, day in enumerate(
        days,
        start=1
    ):

        result.append(
            {
                "day": idx,
                "url":
                    build_day_route_url(
                        day,
                        office_lat,
                        office_lon
                    )
            }
        )

    return result