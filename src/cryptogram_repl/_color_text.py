from ._color_enum import ColorEnum


def color_text(text: str, application: ColorEnum | list[ColorEnum]) -> str:

    colors = "".join([application] if isinstance(application, ColorEnum) else application)

    return f"{colors}{text}{ColorEnum.ENDC}"
