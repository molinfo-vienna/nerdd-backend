import hashlib
import inspect
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, ParamSpec, cast

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response

from .cache_headers import immutable_cache_headers

__all__ = ["ContentHashedAPIRouter"]

P = ParamSpec("P")


def _compute_cache_hash(content: bytes, length: int = 24) -> str:
    """Return a compact, content-addressed cache key suitable for use in URLs."""
    return hashlib.sha256(content).hexdigest()[:length]


class ContentHashedAPIRouter(APIRouter):
    """An API router that can register content-addressed GET routes."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._hash_parameters: dict[str, str] = {}

    def content_hashed_url_for(
        self,
        request: Request,
        endpoint_name: str,
        content: bytes,
        **path_params: Any,
    ) -> str:
        """Return the content-addressed URL for an endpoint and its response body."""
        try:
            hash_parameter = self._hash_parameters[endpoint_name]
        except KeyError as e:
            raise ValueError(f"Unknown content-hashed endpoint: {endpoint_name}") from e

        return str(
            request.url_for(
                endpoint_name,
                **{**path_params, hash_parameter: _compute_cache_hash(content)},
            )
        )

    def content_hashed_get(
        self,
        path: str,
        *,
        hash_parameter: str = "hash",
        **get_options: Any,
    ) -> Callable[
        [Callable[P, Awaitable[Any]]],
        Callable[P, Awaitable[Response]],
    ]:
        """Register a GET route and its hidden, content-addressed variant.

        The decorated endpoint returns a non-streaming Response or JSON-compatible value.
        Requests without the current hash redirect to the content-addressed URL; requests with it
        receive the response with immutable cache headers.
        """

        def decorator(
            function: Callable[P, Awaitable[Any]],
        ) -> Callable[P, Awaitable[Response]]:
            # define the route handler
            async def get_response(
                request: Request,
                requested_hash: str | None,
                *args: P.args,
                **kwargs: P.kwargs,
            ) -> Response:
                # call the actual endpoint function to get the response
                endpoint = cast(Callable[..., Awaitable[Any]], function)
                result = await endpoint(*args, request=request, **kwargs)
                response = (
                    result
                    if isinstance(result, Response)
                    else JSONResponse(content=jsonable_encoder(result))
                )

                if not hasattr(response, "body"):
                    raise TypeError("content_hashed_get does not support streaming responses")

                content = bytes(response.body)
                current_hash = _compute_cache_hash(content)

                # requested hash does not match the hash of the response content
                # -> redirect to the URL with the correct hash (307 Temporary Redirect)
                if requested_hash != current_hash:
                    return RedirectResponse(
                        request.url_for(
                            function.__name__,
                            **{**request.path_params, hash_parameter: current_hash},
                        ),
                        status_code=307,
                        headers={"Cache-Control": "no-store"},
                    )

                response.headers.update(immutable_cache_headers())
                return response

            # define the "normal route" and pass hash=None to the handler (will redirect)
            @wraps(function)
            async def base_route(request: Request, *args: P.args, **kwargs: P.kwargs) -> Response:
                return await get_response(request, None, *args, **kwargs)

            # define the "hashed route" and forward the hash (given in the route) to the handler
            @wraps(function)
            async def hashed_route(request: Request, *args: P.args, **kwargs: P.kwargs) -> Response:
                requested_hash = cast(str, kwargs.pop(hash_parameter))
                return await get_response(
                    request,
                    requested_hash,
                    *args,
                    **kwargs,
                )

            # build the function signatures for the two routes
            signature = inspect.signature(function)
            response_signature = signature.replace(return_annotation=Response)
            base_route.__signature__ = response_signature  # type: ignore[attr-defined]

            hashed_route.__signature__ = response_signature.replace(  # type: ignore[attr-defined]
                parameters=[
                    *response_signature.parameters.values(),
                    inspect.Parameter(
                        hash_parameter,
                        kind=inspect.Parameter.KEYWORD_ONLY,
                        annotation=str,
                    ),
                ]
            )

            # register the two routes with the router
            hashed_path = f"{path}/{{{hash_parameter}}}"
            route_name = get_options.get("name", function.__name__)
            self._hash_parameters[route_name] = hash_parameter
            self.get(path, **get_options)(base_route)
            self.get(hashed_path, include_in_schema=False)(hashed_route)

            return cast(Callable[P, Awaitable[Response]], base_route)

        return decorator
