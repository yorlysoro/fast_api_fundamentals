# Python

from os import stat
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import (BaseModel,
                      Field,
                      EmailStr,
                      HttpUrl)

# FastAPI
from fastapi import (
    FastAPI,
    Body,
    Query,
    Path,
    status,
    Form,
    Header,
    Cookie,
    UploadFile,
    File,
    HTTPException)
from starlette.types import Message

app = FastAPI(debug=True)

# Models


class HairColor(Enum):
    white = "white"
    black = "black"
    brown = "brown"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str = Field(
        min_length=1,
        max_length=50,
        example="Mexico"
    )
    state: str = Field(
        min_length=1,
        max_length=50,
        example="Distrito Capital"
    )
    country: str = Field(
        min_length=1,
        max_length=50,
        example="Mexico"
    )


class PersonBase(BaseModel):
    first_name: str = Field(
        min_length=1,
        max_length=50,
        example="Miguel"
    )
    last_name: str = Field(
        min_length=1,
        max_length=50,
        example="Torres"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example=HairColor.black
    )
    is_married: Optional[bool] = Field(
        default=None,
        example=False
    )
    email: Optional[EmailStr] = Field(
        default=None,
        example="miguel@hola.com"
    )
    website: Optional[HttpUrl] = Field(
        default=None,
        example="https://www.platzi.com"
    )


class Person(PersonBase):
    password: str = Field(..., min_length=8)


class LoginOut(BaseModel):
    username: str = Field(
        ...,
        max_length=20,
        example="miguel2021"
    )
    message: str = Field(
        default="Login successfully!"
    )


@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=["Landing Pages"]
)
def index():
    return {'Hello': 'World!'}


# Request and Response Body

@app.post(
    path="/person/new",
    response_model=PersonBase,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
)
def create_person(person: Person = Body(...)):
    """
    Create Person
    This path operation creates a person in the app and save the information in the database
    Parameters: 
    - Request body parameter: 
        - **person: Person** -> A person model with first name, last name, age, hair color and marital stauts
    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person

# Validaciones: Query Parameters


@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def show_person(name: Optional[str] = Query(None,
                                            min_length=1,
                                            max_length=50,
                                            title="Person Name",
                                            description="This is the person name. It's between 1 and 50 characters",
                                            example="Rocío"),
                age: str = Query(...,
                                 title="Person Age",
                                 description="This is the person age. It's required",
                                 example=25)):
    return {name: age}

# Validaciones: Path parameters


persons = [1, 2, 3, 4, 5]


@app.get(
    path="/person/detail/{person_id}",
    tags=["Persons"]
)
def show_person2(
    person_id: int = Path(
        ...,
        gt=0,
        example=123)):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )
    return {person_id: "It exists!"}

# Validaciones: Request Body


@app.put(
    path="/person/{person_id}",
    tags=["Persons"]
)
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: PersonBase = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


# cookie and headers parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contacts"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent


@app.post(
    path="/post-image",
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }
