from fastapi import Request, HTTPException


def get_current_user(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )

    return request.state.user


def require_admin(request: Request):
    user = get_current_user(request)

    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user