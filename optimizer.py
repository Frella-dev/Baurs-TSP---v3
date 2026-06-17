import pandas as pd

from priority import (
    prepare_customers,
    get_pending_customers
)

from route_engine import (
    build_master_route,
    split_route_by_distance,
    route_summary
)


OFFICE_LAT = 6.8275814230546725
OFFICE_LON = 79.95698659415302


def build_nationwide_plan(
    df,
    daily_limit=160
):
    """
    Generate full Sri Lanka plan
    """

    df = prepare_customers(df)

    df = get_pending_customers(df)

    df = df.sort_values(
        by=[
            "Priority"
        ],
        ascending=False
    )

    route = build_master_route(
        df,
        OFFICE_LAT,
        OFFICE_LON
    )

    days = split_route_by_distance(
        route,
        daily_limit
    )

    return days


def build_area_plan(
    df,
    area,
    daily_limit=160
):
    """
    Generate route for one town/area
    """

    df = prepare_customers(df)

    df = get_pending_customers(df)

    area_df = df[
        df["Town"]
        .astype(str)
        .str.upper()
        ==
        str(area).upper()
    ].copy()

    if len(area_df) == 0:

        return []

    route = build_master_route(
        area_df,
        OFFICE_LAT,
        OFFICE_LON
    )

    days = split_route_by_distance(
        route,
        daily_limit
    )

    return days


def inject_missed_visit1(
    route_day,
    all_customers,
    radius_km=10
):
    """
    Add nearby Visit 1 customers
    when salesperson is already
    in that area.
    """

    from route_engine import haversine

    missed = all_customers[
        all_customers[
            "Pending Visit No"
        ]
        == 1
    ]

    additions = []

    for stop in route_day:

        for _, customer in missed.iterrows():

            distance = haversine(
                stop["Latitude"],
                stop["Longitude"],
                customer["Latitude"],
                customer["Longitude"]
            )

            if distance <= radius_km:

                additions.append(
                    customer.to_dict()
                )

    unique = {}

    for item in additions:

        unique[
            item["Customer name"]
        ] = item

    final = route_day.copy()

    for item in unique.values():

        exists = False

        for stop in route_day:

            if (
                stop["Customer name"]
                ==
                item["Customer name"]
            ):

                exists = True

                break

        if not exists:

            final.append(item)

    return final


def apply_missed_visit_logic(
    days,
    df,
    radius_km=10
):

    enhanced = []

    for day in days:

        enhanced_day = (
            inject_missed_visit1(
                day,
                df,
                radius_km
            )
        )

        enhanced.append(
            enhanced_day
        )

    return enhanced


def create_plan(
    df,
    mode="nationwide",
    area=None,
    daily_limit=160
):

    if mode == "area":

        days = build_area_plan(
            df,
            area,
            daily_limit
        )

    else:

        days = build_nationwide_plan(
            df,
            daily_limit
        )

    df = prepare_customers(df)

    days = apply_missed_visit_logic(
        days,
        df,
        radius_km=10
    )

    return days


def get_plan_summary(
    days
):

    return route_summary(
        days
    )


def get_day_summary(
    days,
    day_no
):

    if day_no < 1:

        return None

    if day_no > len(days):

        return None

    day = days[
        day_no - 1
    ]

    from route_engine import (
        create_day_summary
    )

    return create_day_summary(
        day
    )


def get_day_stops(
    days,
    day_no
):

    if day_no < 1:

        return []

    if day_no > len(days):

        return []

    return days[
        day_no - 1
    ]


def get_next_day_start(
    days,
    day_no
):
    """
    Future support:
    Day N end becomes
    Day N+1 start
    """

    if (
        day_no <= 0
        or
        day_no >= len(days)
    ):

        return None

    previous_day = days[
        day_no - 1
    ]

    if len(previous_day) == 0:

        return None

    return previous_day[-1]