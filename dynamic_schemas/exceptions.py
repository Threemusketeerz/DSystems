""" Custom exceptions for more precise handling of wanted errors """

class SchemaIsLockedError(Exception):
    """ Raise if Schema is locked, and admin is trying to save or delete """
    pass
