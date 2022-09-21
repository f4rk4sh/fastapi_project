import pytest
from sqlalchemy.orm import Session

from app.crud.crud_role import CRUDRole
from app.db.models import Role


@pytest.fixture(scope="module")
def override_crud_role(db: Session):
    crud_role: CRUDRole = CRUDRole(Role, db)
    return crud_role
