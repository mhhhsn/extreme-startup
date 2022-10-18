from request_sugar_aliases import *

import sys

sys.path.append(".")

from flaskr import app

GET = 0
POST = 1
PUT = 2
DELETE = 3

ALL_GOOD = 200
FAULTY_REQUEST = 400
NOT_FOUND = 404
METHOD_NOT_ALLOWED = 405
ERROR_501 = 501
DELETE_SUCCESS = 204


def setup_server_with(client, server_setup):
    """Gets a list of tuples representing a request and returns a list of
    corresponding responses"""
    setup_extras = []
    for (method, url, data, query_str) in server_setup:
        get_response_by_request_method = {
            GET: lambda: client.get(url, query_string=query_str),
            POST: lambda: client.post(url, data=data, query_string=query_str),
            PUT: lambda: client.put(url, data=data, query_string=query_str),
            DELETE: lambda: client.delete(url, query_string=query_str),
        }
        rd = response_as_dict(get_response_by_request_method[method]())
        setup_extras.append(rd)
    return setup_extras


def with_setup(server_setup=None, **callable_setup_kwargs):
    """Decorator Wrapper for testing functions.
    This sends some pre-emptive "server_setup" requests and does a final
    request, letting the test function verify the response.
    Args:
    - server_setup: a list of tuples corresponding to requests
                    to be sent to server before the test one.
        See setup_server_with"""
    if server_setup is None:
        server_setup = []

    def inner(test_func):
        def wrapper():
            # Connect to our flask app.
            app.config.update({"TESTING": True})
            client = app.test_client()

            # Pre-populate with some requests
            if callable(server_setup):
                setup_extras = server_setup(client, **callable_setup_kwargs)
            else:
                setup_extras = setup_server_with(client, server_setup)

            test_func(setup_extras, client)

        return wrapper

    return inner


create_a_couple_of_games = ((POST, "/", None, None), (POST, "/", None, None))


def create_a_game_with_players(cli, num_players=2):
    game = create_game(cli)
    gid = game["id"]

    print("gid", gid)

    players = {}
    for _ in range(num_players):
        curr_player = create_player(cli, gid)
        players[curr_player["id"]] = curr_player

    return {"game": game, "players": players}
