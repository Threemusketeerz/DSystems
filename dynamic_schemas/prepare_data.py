from io import StringIO

from .models import SchemaResponse, SchemaColumn

import json


def getcolumns(schemaresponse):
    """ Fetches columns dynamically instead of being reliant on javascript
    file.
    A bit clumsy right now, but it works.
    """
    # We want id first, hopefully we can hide it though -> then append the rest
    # on it.
    column_set = [
        {"data": "id", "title": "ID"},
        ]
    
    for c, d in schemaresponse.__dict__.items():
        if type(d) is dict:
            for x in d:
                column = {}
                column["data"] = c + '.' + x
                column["title"] = x 
                column_set.append(column)
                # import ipdb; ipdb.set_trace()
            # print(d)

    column_set.append(
        {"data": "instruction", "title": "Instruktion"}
        )

    column_set.append(
        {"data": "user", "title": "Bruger"}
        )

    column_set.append(
        {"data": "pub_date", "title": "Dato"}
        )

    io = StringIO()
    json.dump(column_set, io)

    return io
