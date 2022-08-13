# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, Body, Query, Path

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


class Person(BaseModel):
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


@app.get('/')
def index():
    return {'Hello': 'World!'}


# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters


@app.get('/person/detail')
def show_person(name: Optional[str] = Query(None,
                                            min_length=1,
                                            max_length=50,
                                            title="Person Name",
                                            description="This is the person name. It's between 1 and 50 characters"),
                age: str = Query(...,
                                 title="Person Age",
                                 description="This is the person age. It's required")):
    return {name: age}

# Validaciones: Path parameters


@app.get("/person/detail/{person_id}")
def show_person2(person_id: int = Path(..., gt=0)):
    return {person_id: "It exists!"}

# Validaciones: Request Body


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
