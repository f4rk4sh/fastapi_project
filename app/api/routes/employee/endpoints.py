from typing import Optional, List

from fastapi_utils.inferring_router import InferringRouter
from fastapi import status
from pydantic.types import PositiveInt

from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.manager.manager_employee import employee
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler
from app.schemas.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employees"])
descriptions = CRUDEndpointsDescriptions(
    model_name="Employee",
    search_parameters=["email", "phone", "fullname", "passport", "tax_id", "birth_date"]
)
params = CRUDParamsDescriptions(obj_name="Employee")


@router.get("/employee", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_employees() -> List[EmployeeResponse]:
    return employee.fetch_all()


@router.get("/employee/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_employees(
        parameter: str = params.search_parameter,
        keyword: str = params.search_keyword,
        max_results: Optional[PositiveInt] = params.max_results_search
) -> List[EmployeeResponse]:
    return employee.search(parameter, keyword, max_results)


@router.post("/employee", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_employee(employee_in: EmployeeCreate) -> EmployeeResponse:
    return employee.create(employee_in)


@router.put("/employee", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_employee(employee_in: EmployeeUpdate) -> EmployeeResponse:
    return employee.update(employee_in)


@router.get("/employee/{employee_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_employee(employee_id: PositiveInt = params.get_id) -> EmployeeResponse:
    return employee.fetch_one(employee_id)


@router.delete("/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
def delete_employee(employee_id: PositiveInt = params.delete_id):
    return employee.delete(employee_id)
