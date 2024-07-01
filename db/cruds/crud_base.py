"""Base file for crud operation"""
from typing import Any, Generic, TypeAlias, TypeVar

from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from book_summarizer.db.models.base_class import Base
from book_summarizer.utils.exception_utils import AlreadyExistsError

ModelType: TypeAlias = TypeVar("ModelType", bound=Base)
CreateSchemaType: TypeAlias = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType: TypeAlias = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations."""

    def __init__(self, model: type[ModelType], primary_column: str = "id"):
        """Initializes the variables."""
        self.model = model
        self.primary_column = primary_column

    async def get(self, db: AsyncSession, search_value: str) -> ModelType | None:
        """Get first entry that matches search value by the primary column."""
        query = select(self.model).filter(getattr(self.model, self.primary_column) == search_value)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> list[ModelType] | None:
        """Get all entries."""
        query = select(self.model)
        result = await db.execute(query)
        return result.scalars().all()

    async def create_with_name(
        self,
        db: AsyncSession,
        obj_inputs: list[CreateSchemaType],
        resource_type: str | None = "",
    ) -> list[ModelType]:
        """Create entries with unique names."""
        existing_names = await self.check_name_exists(db, obj_inputs)
        existing_names = [str(obj) for obj in existing_names]
        if existing_names:
            existing_names_str = ", ".join("'" + item + "'" for item in existing_names)
            raise AlreadyExistsError(
                f"{resource_type} {existing_names_str} already exists in table. Please consider renaming"
            )
        return await self.create(db=db, obj_inputs=obj_inputs)

    async def create(self, db: AsyncSession, obj_inputs: list[CreateSchemaType]) -> list[ModelType]:
        """Create entries in the database table."""
        obj_in_data = [self.model(**obj_in.dict()) for obj_in in obj_inputs]
        db.add_all(obj_in_data)
        await db.commit()
        return obj_in_data

    async def update(self, db: AsyncSession, obj_in: UpdateSchemaType) -> UpdateSchemaType:
        """Update an entry in the database table."""
        obj_in_data = obj_in.dict(exclude_unset=True)
        query = select(self.model).filter(getattr(self.model, self.primary_column) == obj_in_data[self.primary_column])
        result = await db.execute(query)
        db_obj = result.scalar_one_or_none()
        if db_obj:
            for key, value in obj_in_data.items():
                setattr(db_obj, key, value)
            await db.commit()
            await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id_value: str) -> ModelType:
        """Delete an entry in the database table."""
        query = select(self.model).filter(getattr(self.model, self.primary_column) == id_value)
        result = await db.execute(query)
        obj = result.scalar_one_or_none()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

    async def delete_by_multiple_columns(self, db: AsyncSession, search_dict: dict[str, Any]) -> list[ModelType]:
        """Delete entries in the database table by searching multiple columns."""
        query = select(self.model).filter(
            *(getattr(self.model, column_name) == str(search_value) for column_name, search_value in search_dict.items())
        )
        result = await db.execute(query)
        all_objs = result.scalars().all()
        for obj in all_objs:
            await db.delete(obj)
        await db.commit()
        return all_objs

    async def check_name_exists(self, db: AsyncSession, obj_inputs: list[Any]) -> list[str]:
        """Check if the primary ids already exist in the database table."""
        new_primary_ids = [obj_in.__dict__[self.primary_column] for obj_in in obj_inputs]
        query = select(self.model).filter(getattr(self.model, self.primary_column).in_(new_primary_ids))
        result = await db.execute(query)
        existing_names = [i.__dict__[self.primary_column] for i in result.scalars().all()]
        return existing_names
    
    async def get_multiple(self, db: AsyncSession, obj_inputs: list[str]) -> list[Any]:
        """Get multiple objects by searching a list of strings."""
        query = select(self.model).filter(getattr(self.model, self.primary_column).in_(obj_inputs))
        result = await db.execute(query)
        return result.scalars().all()

    async def delete_multiple(self, db: AsyncSession, obj_inputs: list[str]) -> list[Any]:
        """Delete multiple objects by searching a list of strings."""
        query = select(self.model).filter(getattr(self.model, self.primary_column).in_(obj_inputs))
        result = await db.execute(query)
        all_objs = result.scalars().all()
        for obj in all_objs:
            await db.delete(obj)
        await db.commit()
        return all_objs

    async def get_missing_ids(self, db: AsyncSession, obj_inputs: list[Any]) -> list[str]:
        """Search if all input objects exist or not."""
        new_ids = [obj.__dict__[self.primary_column] for obj in obj_inputs]
        existing_ids = await self.check_name_exists(db=db, obj_inputs=obj_inputs)
        missing_ids = [ids for ids in new_ids if ids not in existing_ids]
        return missing_ids

    async def update_multiple(self, db: AsyncSession, obj_inputs: list[UpdateSchemaType]) -> list[UpdateSchemaType]:
        """Update multiple entries in the database table."""
        # Checking if all the input update objects exist in table or not.
        update_ids = [obj_in.__dict__[self.primary_column] for obj_in in obj_inputs]
        missing_ids = await self.get_missing_ids(db=db, obj_inputs=obj_inputs)
        # Raise error if any object is missing in table
        if missing_ids:
            missing_id_str = ", ".join("'" + item + "'" for item in missing_ids)
            error_msg = (f"{self.primary_column}(s) {missing_id_str} do not exist."
                         f" Please provide correct {self.primary_column}.")
            raise ValueError(error_msg)

        # If all objects exist in database, start the update procedure.
        all_objs = await self.get_multiple(db=db, obj_inputs=update_ids)
        for count, orig_obj in enumerate(all_objs):
            # Getting the update dictionary and setting the value
            update_obj = obj_inputs[count].dict(exclude_unset=True)
            for key, value in update_obj.items():
                setattr(orig_obj, key, value)
        await db.commit()
        return all_objs

    async def search_by_multiple_column(
        self,
        db: AsyncSession,
        search_dict: dict[str, Any],
        page: int | None = None,
        size: int | None = None,
        order_by: str | None = None,
        reverse: bool | None = False,
    ) -> list[ModelType]:
        """Get entries that match search value by multiple columns."""
        query = select(self.model).filter(
            *(getattr(self.model, column_name) == search_value for column_name, search_value in search_dict.items())
        )
        if page and size:
            if order_by:
                query = query.order_by(getattr(self.model, order_by))
            if order_by and reverse:
                query = query.order_by(getattr(self.model, order_by).desc())
            # return await paginate(query=query, conn=db, params=Params(page=page
            return await paginate(query=query, conn=db, params=Params(page=page, size=size))

        result = await db.execute(query)
        return result.scalars().all()

    async def get_from_list(self, db: AsyncSession, search_value: str, column_name: str) -> list[ModelType] | None:
        """Get all entries that contain search value in a specific column."""
        query = select(self.model).filter(getattr(self.model, column_name).any(search_value))
        result = await db.execute(query)
        return result.scalars().all()

