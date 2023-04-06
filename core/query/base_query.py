import datetime
import typing as t
import uuid
import ormar
import pydantic
from core.enum.sort_type import SortOrder
from lib.exceptions.invalid_parameter_error import InvalidParameterError
from lib.exceptions.not_found_error import NotFoundError
from lib.exceptions.server_error import ServerError
from lib.db.model import BaseModel
from lib.utils.random_string import random_str

ModelType = t.TypeVar("ModelType", bound=BaseModel)


class BaseQuery(t.Generic[ModelType]):
    def __init__(self, model_cls: ModelType):
        self.model = model_cls

    def make_slug(self, name: str, random_length: int = 10) -> str:
        slug = f"{name.replace(' ', '-').replace('_', '-')[:30]}-{random_str(random_length).strip().lower()}"
        return slug

    def make_select_from_str(self, select: str = "") -> t.List[str]:
        select = [item.strip() for item in select.split(",") if select is not None]
        return select

    async def get_by_attr(
        self, first: bool = True, load_related: bool = False, **kwargs
    ) -> t.Union[t.List[ModelType], ModelType]:
        query = self.model.objects
        if load_related:
            query = query.select_all()
        if first:
            return await query.get_or_none(**kwargs)
        return await query.filter(**kwargs).all()

    async def get_by_props(
        self,
        first: bool = True,
        load_related: bool = False,
        prop_name: str = None,
        prop_value: t.List[t.Union[str, uuid.UUID]] = [],
    ) -> t.Union[t.List[ModelType], ModelType]:
        query = self.model.objects
        if load_related:
            query = query.select_all()
        if first:
            return await query.filter(
                f"{getattr(self.model, prop_name)}_in({prop_value})"
            ).first()
        return await query.filter(
            f"{getattr(self.model, prop_name)}_in({prop_value})"
        ).all()

    async def create_obj(self, data_in: t.Union[dict, pydantic.BaseModel]) -> ModelType:
        if isinstance(data_in, dict):
            for k, v in data_in.items():
                if not hasattr(self.model, k):
                    del data_in[k]
                new_obj = await self.model.objects.create(**data_in)
            if new_obj:
                return new_obj
            raise ServerError("Error creating obj")
        if isinstance(data_in, pydantic.BaseModel):
            data = data_in.dict().items()
            for k, v in data:
                if not hasattr(self.model, k):
                    del data_in[k]
            new_obj = await self.model.objects.create(**data)
            if new_obj:
                return new_obj
            raise ServerError("Error creating obj")

    async def bulk_create_obj(
        self, data_in: t.Union[t.List[dict], t.List[pydantic.BaseModel]]
    ) -> ModelType:
        to_create = []
        for obj in data_in:
            if isinstance(data_in, dict):
                for k, v in data_in.items():
                    if hasattr(self.model, k):
                        to_create.append(obj)
            elif isinstance(data_in, pydantic.BaseModel):
                for k, v in data_in.dict().items():
                    if hasattr(self.model, k):
                        to_create.append(obj)
            else:
                raise InvalidParameterError(
                    f"Invalid parameter expected, dict or {self.model.__class__.__name__}"
                )
        if await self.model.objects.bulk_create(to_create):
            return True
        return None

    async def update_obj(
        self, obj_id: uuid.UUID, data_in: t.Union[dict, pydantic.BaseModel]
    ) -> ModelType:
        check_perm = await self.model.objects.get_or_none(id=obj_id)
        if not check_perm:
            raise NotFoundError("Permission not found")
        if isinstance(data_in, dict):
            for k, v in data_in.items():
                if hasattr(self.model, k):
                    setattr(check_perm, k, v)
                    result = await check_perm.upsert()
                    if result:
                        return result
                    raise ServerError("Error updating obj")
        if isinstance(data_in, pydantic.BaseModel):
            for k, v in data_in.dict().items():
                if hasattr(self.model, k):
                    setattr(check_perm, k, v)
                    result = await check_perm.upsert()
                    if result:
                        return result
                    raise ServerError("Error updating obj")

    async def filter(
        self,
        filter_string: str,
        load_related: bool = True,
        page: int = 1,
        page_size: int = 20,
        strict_search: dict = {},
        select_columns: t.Optional[t.Union[t.List[str], str]] = None,
        order_by: t.Optional[t.Union[t.List[str], str]] = None,
        sort_by: SortOrder = SortOrder.asc,
    ) -> dict:
        query_set = self.model.objects
        # if load_related:
        #     query_set = query_set.select_related("*")
        # Loop through each field in the model and apply the filter
        for field_name, field_obj in self.model.Meta.model_fields.items():
            # Check if the field is a relationship
            if field_obj.is_relation:
                #     # Filter the query set by the related model's string representation
                related_model_cls = field_obj.to
                print(
                    [col for col, name in related_model_cls.Meta.model_fields.items()]
                )
            #     related_model_ids = [
            #         obj.id
            #         for obj in await related_model_cls.objects.filter(
            #             __str__=filter_string
            #         )
            #     ]

            #     query_set = query_set.filter(
            #         ormar.or_(**strict_search),
            #         **{f"{field_name}__in": related_model_ids},
            #     )

            # # If the field is not a relationship, check its type and filter accordingly
            # else:
            field_type = field_obj.__class__.__name__
            if field_type == "UUIDField":
                # Convert the string filter_string to a UUID object
                filter_string = uuid.UUID(filter_string)
            elif field_type == "DateTimeField":
                # Convert the string filter_string to a datetime object
                filter_string = datetime.fromisoformat(filter_string)
            elif field_type == "DateField":
                # Convert the string filter_string to a date object
                filter_string = datetime.strptime(filter_string, "%Y-%m-%d").date()
            elif field_type == "TimeField":
                # Convert the string filter_string to a time object
                filter_string = datetime.strptime(filter_string, "%H:%M:%S").time()
            elif field_type in ["IntegerField", "FloatField"]:
                # Check if filter_string is less than a particular number
                if filter_string.startswith("<"):
                    try:
                        num = float(filter_string[1:])
                        query_set = query_set.filter(
                            ormar.or_(**strict_search),
                            **{f"{field_name}__lt": num},
                        )
                    except ValueError:
                        pass
            # Filter the query set by the field's filter_string
            query_set = query_set.filter(
                ormar.or_(**strict_search),
                **{field_name: filter_string},
            )
        # Select columns if specified
        order_by = self.make_select_from_str(order_by)
        if sort_by.lower() == SortOrder.asc:
            if isinstance(order_by, str):
                query_set = query_set.order_by(f"-{order_by}")
            else:
                query_set = query_set.order_by(*[f"-{value}" for value in order_by])
        else:
            if isinstance(order_by, str):
                query_set = query_set.order_by(order_by)
            else:
                query_set = query_set.order_by(*order_by)

        select_columns = self.make_select_from_str(select_columns)
        if select_columns:
            if isinstance(select_columns, str):
                query_set = query_set.filter_strings(
                    ormar.or_(**strict_search),
                    *select_columns,
                )
            else:
                if len(select_columns) == 1:
                    query_set = query_set.values(
                        ormar.or_(**strict_search),
                        *select_columns,
                    )
                else:
                    query_set = query_set.values(
                        ormar.or_(**strict_search),
                        select_columns,
                    )
        # result = await query_set()
        # # Order by columns if specified

        # Return the resulting models
        # result = await query_set
        # if result:
        #     # Count total number of objects
        #     total_count = await result.count()

        #     # Calculate offset and limit for pagination
        #     offset = (page - 1) * page_size
        #     limit = page_size

        #     # Apply offset and limit
        #     query = query.offset(offset).limit(limit)

        #     # Execute the query and retrieve the objects
        #     objects = await query.all()

        #     # Check if there are more pages
        #     has_next = (offset + limit) < total_count
        #     has_previous = offset > 0
        #     # Raise an exception if the requested page does not exist
        #     if page > 1 and not objects:
        #         raise NotFoundError("Page not found")

        #     return {
        #         "items": objects,
        #         "total": total_count,
        #         "page": page,
        #         "page_size": page_size,
        #         "has_next": has_next,
        #         "has_previous": has_previous,
        #         "next_page": page + 1 if has_next else None,
        #         "previous_page": page - 1 if has_previous else None,
        #     }

        # return []

    async def get_count(self) -> t.Optional[int]:
        if not issubclass(self.model, ModelType):
            return None
        manager = self.model.objects
        count = await manager.count()
        return count

    async def delete_obj(self, obj_id: uuid.UUID) -> None:
        check_perm = await self.model.objects.get_or_none(id=obj_id)
        if not check_perm:
            raise NotFoundError("Permission not found")
        return await check_perm.delete()
