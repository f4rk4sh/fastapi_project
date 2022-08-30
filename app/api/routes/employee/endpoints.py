from typing import Optional

from fastapi_utils.inferring_router import InferringRouter
from fastapi import status, Response
from pydantic.types import PositiveInt

from app import crud
from app.api.routes.descriptions.employee_params_description import employee_params
from app.core.documentation.openapi_descriptions import CRUDDescriptions
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.db.models import Employee
from app.schemas.employee import EmployeesResponse, EmployeeSearchResponse, EmployeeCreate, EmployeeResponse, \
    EmployeeUpdate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employees"])
descriptions = CRUDDescriptions(model=Employee, search_parameters=["fullname", "passport", "tax_id", "birth_date"])


@router.get("/employee", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_employees() -> EmployeesResponse:
    employees = crud.employee.get_multi()
    return EmployeesResponse(employees=employees)


@router.get("/employee/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_employees(
        parameter: str = employee_params.search_parameter,
        keyword: str = employee_params.search_keyword,
        max_results: Optional[PositiveInt] = employee_params.max_results_search
) -> EmployeeSearchResponse:
    results = crud.employee.search_by_parameter(parameter=parameter, keyword=keyword, limit=max_results)
    return EmployeeSearchResponse(results=results)


@router.post("/employee", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_employee(employee_in: EmployeeCreate) -> EmployeeResponse:
    employee = crud.employee.create(obj_in=employee_in)
    return EmployeeResponse.from_orm(employee)


@router.put("/employee", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_employee(employee_in: EmployeeUpdate) -> EmployeeResponse:
    employee = crud.employee.get(id=employee_in.id)
    updated_employee = crud.employee.update(db_obj=employee, obj_in=employee_in)
    return EmployeeResponse.from_orm(updated_employee)


@router.get("/employee/{employee_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_employee(employee_id: PositiveInt = employee_params.get_id) -> EmployeeResponse:
    employee = crud.employee.get(id=employee_id)
    return EmployeeResponse.from_orm(employee)


@router.delete("/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
def delete_employee(employee_id: PositiveInt = employee_params.delete_id):
    crud.employee.delete(id=employee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
