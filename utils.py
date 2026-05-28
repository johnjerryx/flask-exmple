from sqlalchemy.sql import Executable

def extract_app_token(header_value: str) -> str | None:
    """Extracts and cleans the token in a single string scan."""
    # If "Bearer " isn't found, rpartition returns: ('', '', header_value)
    # The middle variable (_) will be empty if "Bearer " is missing.
    left, found, token_part = header_value.rpartition("Bearer ")
    
    if not found:
        return None

    # Split on comma, grab the token, and strip whitespace in one go
    token = token_part.split(",", 1)[0].strip()

    return token if token else None


def paginate(stmt: Executable, page: int, per_page: int = 20) -> Executable:
    return stmt.limit(per_page).offset((page - 1) * per_page)