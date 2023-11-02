from typing import TypeVar, Callable, Any, Awaitable, Union

AF = TypeVar("AF", bound=Callable[..., Awaitable[Any]])
F = TypeVar("F", bound=Callable[..., Any])
Json = Union[dict, list]
