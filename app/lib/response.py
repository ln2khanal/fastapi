from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

templates = Jinja2Templates(directory="app/static/templates")


def prepare_template_response(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)


def prepare_json_response(data: dict):
    # we cain inject pre-reponse activities here
    return JSONResponse(content={"data": data})
