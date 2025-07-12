import base64
import datetime
import json
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import altcha
from fastapi import APIRouter, HTTPException, Query, Request

from ..data import RecordNotFoundError, Repository
from ..models import Challenge

__all__ = ["challenges_router", "verify_solution"]

challenges_router = APIRouter(prefix="/challenges")


@challenges_router.get("/create", include_in_schema=False)
async def create_challenge(request: Request = None):
    app = request.app
    config = app.state.config
    repository = app.state.repository

    # delete all expired challenges
    await repository.delete_expired_challenges(datetime.now(timezone.utc))

    # create new altcha challenge
    options = altcha.ChallengeOptions(
        expires=(
            datetime.now(timezone.utc) + timedelta(seconds=config.challenge_expiration_seconds)
        ),
        max_number=config.challenge_difficulty,
        hmac_key=config.challenge_hmac_key,
    )

    challenge = altcha.create_challenge(options)

    # store the challenge in the repository
    await repository.create_challenge(
        Challenge(
            id=str(uuid4()),
            salt=challenge.salt,
            expires_at=options.expires,
        )
    )

    return challenge.__dict__


@challenges_router.get("/verify", include_in_schema=False)
async def verify_solution(
    payload: str = Query(alias="altcha"),
    request: Request = None,
):
    app = request.app
    config = app.state.config
    repository: Repository = app.state.repository

    # delete all expired challenges
    await repository.delete_expired_challenges(datetime.now(timezone.utc))

    # check that the solution is valid
    valid, error = altcha.verify_solution(
        payload, hmac_key=config.challenge_hmac_key, check_expires=False
    )

    if not valid:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid solution: {error}",
        )

    # extract the altcha parameters (salt, etc.) from the payload
    payload_bytes = base64.b64decode(payload).decode("utf-8")
    try:
        payload_data = json.loads(payload_bytes)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid payload format: {e}",
        ) from e

    # check that the solution wasn't solved before (to prevent replay attacks)
    try:
        challenge = await repository.get_challenge_by_salt(salt=payload_data["salt"])
    except RecordNotFoundError as e:
        raise HTTPException(
            status_code=400,
            detail="Challenge not found or already solved.",
        ) from e

    # delete the challenge from the repository
    await repository.delete_challenge_by_id(challenge.id)

    return "Challenge verified successfully."
