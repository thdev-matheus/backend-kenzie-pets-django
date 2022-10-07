def validate_fields_request(data: dict) -> dict:
    result = {}

    for key in data.keys():
        if key == "group":
            result["group"] = "You can not update group property."
        elif key == "traits":
            result["traits"] = "You can not update traits property."
        elif key == "sex":
            result["sex"] = "You can not update sex property."

    return result
