from fastapi import Query
from fastapi_pagination import Page as BasePage
from fastapi_pagination.customization import UseParamsFields, CustomizedPage


Page = CustomizedPage[
    BasePage,
    UseParamsFields(
        size=Query(15, ge=0),
    ),
]