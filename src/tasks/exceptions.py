class TaskNotFound(Exception):
    def __init__(self, message="Task not found"):
        self.message = message
        
        
class TaskUserHasNotPermission(Exception):
    def __init__(self, message="User does not have permission"):
        self.message = message
        

class TaskUserIsNotAnCollaborator(Exception):
    def __init__(self, message="User is not an collaborator"):
        self.message = message
        