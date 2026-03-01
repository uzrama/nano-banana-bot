from typing import Any, ClassVar

from pydantic import BaseModel
from pydantic import ConfigDict, PrivateAttr


class PydanticModel(BaseModel):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="ignore",
        from_attributes=True,
        populate_by_name=True,
    )


class ActiveRecordModel(PydanticModel):
    __updated: dict[str, Any] = PrivateAttr(default_factory=dict)

    @property
    def model_state(self) -> dict[str, Any]:
        return self.__updated

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        self.__updated[name] = value
