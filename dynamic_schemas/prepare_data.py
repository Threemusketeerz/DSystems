from .models import SchemaResponse, SchemaColumn


def get_columns(schemaresponse):
    for c, d in sr.__dict__.items():
        if type(d) is dict:
            print(d)
        else:
            print(c)


