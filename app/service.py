from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PhoneBook
from app.schemas import ContactCreate


class ContactNotFoundError(Exception):
    pass


class DuplicateContactError(Exception):
    pass


class ContactService:
    def __init__(self, session: Session):
        self.session = session

    def add_contact(self, data: ContactCreate) -> PhoneBook:
        contact = PhoneBook(**data.model_dump())
        existing = self.session.scalar(select(PhoneBook).where(PhoneBook.mobile == contact.mobile))
        if existing is not None:
            raise DuplicateContactError(
                "Contact with this phone already exists"
            )

        try:
            self.session.add(contact)
            self.session.commit()
            self.session.refresh(contact)
            return contact
        except Exception:
            self.session.rollback()
            raise

    def get_all(self) -> list[PhoneBook]:
        statement = select(PhoneBook)
        return list(self.session.scalars(statement).all())

    def get_by_id(self, contact_id: int) -> PhoneBook:
        contact = self.session.get(PhoneBook, contact_id)

        if contact is None:
            raise ContactNotFoundError(
                f"Contact {contact_id} not found"
            )

        return contact

    def del_contact(self, contact_id: int) -> PhoneBook:
        contact = self.session.get(PhoneBook, contact_id)

        if contact is None:
            raise ContactNotFoundError(
                f"Contact {contact_id} not found"
            )

        try:
            self.session.delete(contact)
            self.session.commit()
            return contact
        except Exception:
            self.session.rollback()
            raise

    def put_contact(self, contact_id: int, contact_data: ContactCreate) -> PhoneBook:
        contact = self.session.get(PhoneBook, contact_id)

        if contact is None:
            raise ContactNotFoundError(
                f"Contact {contact_id} not found"
            )

        contact.name = contact_data.name
        contact.mobile = contact_data.mobile
        contact.email = contact_data.email
        self.session.commit()
        self.session.refresh(contact)

        return contact


def get_contact_service(session: Session = Depends(get_db)) -> ContactService:
    return ContactService(session)