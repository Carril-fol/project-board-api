class ProjectNotFoundError(Exception):
    pass


class ProjectInsufficientPrivileges(Exception):
    pass


class ProjectAlreadyHasStatus(Exception):
    pass