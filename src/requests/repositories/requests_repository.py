from sqlalchemy.orm import Session

from ..models.requests_model import Request


class RequestsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, requests: Request) -> Request:
        self.db.add(requests)
        self.db.flush()
        return requests

    def update(self, requests: Request) -> Request:
        self.db.add(requests)
        self.db.flush()
        return requests

    def get_request_by_id(self, request_id: int) -> Request | None:
        request = self.db.query(Request).filter(Request.id == request_id).first()
        return request

    def get_requests_by_project_id(self, project_id: int) -> list[Request]:
        requests = self.db.query(Request).filter(Request.project_id == project_id).all()
        return requests
