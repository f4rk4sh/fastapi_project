from app.schemas.role import RoleCreate, RoleUpdate
from app.tests.utils.base import random_string


def test_create_role_from_schema(override_crud_role):
    name = random_string()
    role = override_crud_role.create(RoleCreate(name=name))
    assert role
    assert role.name == name


def test_create_role_from_dict(override_crud_role):
    name = random_string()
    role = override_crud_role.create({"name": name})
    assert role
    assert role.name == name


def test_get_role(override_crud_role):
    role = override_crud_role.create(RoleCreate(name=random_string()))
    role_in_db = override_crud_role.get(role.id)
    assert role_in_db
    assert role_in_db.id == role.id
    assert role_in_db.name == role.name


def test_get_multiple_roles(override_crud_role):
    roles = [override_crud_role.create(RoleCreate(name=random_string())) for _ in range(3)]
    roles_in_db = override_crud_role.get_multi()
    assert roles_in_db
    for role in roles:
        assert role in roles_in_db


def test_get_role_by_attribute(override_crud_role):
    role = override_crud_role.create(RoleCreate(name=random_string()))
    role_in_db = override_crud_role.get_by_attribute(name=role.name)
    assert role_in_db
    assert role_in_db.id == role.id
    assert role_in_db.name == role.name


def test_search_roles_by_parameter(override_crud_role):
    role = override_crud_role.create(RoleCreate(name=random_string()))
    roles_in_db = override_crud_role.search_by_parameter(parameter="name", keyword=role.name)
    assert roles_in_db
    assert role in roles_in_db


def test_update_role_from_schema(override_crud_role):
    role = override_crud_role.create(RoleCreate(name=random_string()))
    role_in_db = override_crud_role.get(role.id)
    new_name = random_string()
    updated_role = override_crud_role.update(role_in_db, RoleUpdate(id=role.id, name=new_name))
    assert updated_role
    assert updated_role.name == new_name


def test_update_role_from_dict(override_crud_role):
    role = override_crud_role.create(RoleCreate(name=random_string()))
    role_in_db = override_crud_role.get(role.id)
    new_name = random_string()
    updated_role = override_crud_role.update(role_in_db, {"id": role.id, "name": new_name})
    assert updated_role
    assert updated_role.name == new_name


def test_delete_role(override_crud_role):
    role = override_crud_role.create(RoleCreate(name=random_string()))
    override_crud_role.delete(role.id)
    role_in_db = override_crud_role.get_by_attribute(id=role.id)
    assert not role_in_db
