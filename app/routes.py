from fastapi import APIRouter, HTTPException, Depends

from app.schemas import ContactCreate, ContactResponse
from app.service import get_contact_service, ContactService, DuplicateContactError, ContactNotFoundError


router = APIRouter()

@router.get("/contacts", response_model=list[ContactResponse])
def contacts(service: ContactService = Depends(get_contact_service)):
    return service.get_all()

@router.get("/contacts/{id}",  response_model=ContactResponse)
def contact(id: int, service: ContactService = Depends(get_contact_service)):
    try:
        return service.get_by_id(id)
    except ContactNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Contact {id} not found"
        )

@router.post("/contacts", response_model=ContactResponse)
def add_contact(data: ContactCreate, service: ContactService = Depends(get_contact_service)):
    try:
        return service.add_contact(data)
    except DuplicateContactError:
        raise HTTPException(
            status_code=409,
            detail="Contact with this phone already exists"
        )

@router.put("/contacts/{id}", response_model=ContactResponse)
def put_contact(id: int, contact: ContactCreate, service: ContactService = Depends(get_contact_service)):
    try:
        return service.put_contact(id, contact)
    except ContactNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Contact {id} not found"
        )

@router.delete("/contacts/{id}", response_model=ContactResponse)
def del_contact(id: int, service: ContactService = Depends(get_contact_service)):
    try:
        return service.del_contact(id)
    except ContactNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Contact {id} not found"
        )