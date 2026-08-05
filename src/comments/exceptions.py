class CommentUserIsNotFromProject(Exception):
    def __init__(self, message="User is not a collaborator from the project"):
        self.message = message


class CommentNotFound(Exception):
    def __init__(self, message="Comment not found"):
        self.message = message
        

class CommentUserHasNoPrivileges(Exception):
    def __init__(self, message="Permission denied"):
        self.message = message


class CommentTaskNotFound(Exception):
    def __init__(self, message="Task not found"):
        self.message = message
        
    