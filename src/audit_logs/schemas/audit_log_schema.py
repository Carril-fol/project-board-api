from typing import Optional, Any
from pydantic import BaseModel, Field


class AuditLogOutputSchema(BaseModel):
    id: int = Field(..., description="Unique identifier of the audit log entry")
    user_id: int = Field(..., description="ID of the user who performed the action")
    action: str = Field(..., description="Description of the action performed (e.g., 'task_status_update')")
    entity_type: str = Field(..., description="Type of the entity affected (e.g., 'Task', 'Project')")
    entity_id: int = Field(..., description="ID of the affected entity")

    old_value: Optional[dict[str, Any]] = Field(
        None,
        description="The state of the entity before the change. Null if it's a creation event."
    )
    new_value: Optional[dict[str, Any]] = Field(
        None,
        description="The state of the entity after the change. Null if it's a deletion event."
    )

    class Config:
        from_attributes = True

        
class ListAuditLogOutputSchema(BaseModel):
    logs: list[AuditLogOutputSchema] = Field(..., description="List of audit log entries for a specific entity")