from pydantic import constr


NonEmptyString = constr(strip_whitespace=True, min_length=1)

PwdStr = constr(strip_whitespace=True, min_length=6)
