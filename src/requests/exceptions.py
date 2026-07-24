class RequestNotFound(Exception):
    pass


class RequestAlreadyExists(Exception):
    pass


class RequestAlreadyRespondedError(Exception):
    pass


class ProjectNotFoundError(Exception):
    pass


class CollaboratorAlreadyExists(Exception):
    pass
