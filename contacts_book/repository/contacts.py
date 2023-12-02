from typing import List
from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from contacts_book.database.models import Contact
from contacts_book.schemas import ContactModel



async def get_contacts(limit: int, offset: int, search: str|None, db: Session) -> List[Contact]:
    if search:
        return db.query(Contact).filter(or_(Contact.firstname.icontains(search), Contact.lastname.icontains(search), Contact.email.icontains(search))).limit(limit).offset(offset).all()
    
    return db.query(Contact).limit(limit).offset(offset).all()


async def get_contact_by_id(contact_id: int, db: Session) -> Contact|None:
    return db.query(Contact).filter_by(id=contact_id).first()


async def get_contact_by_unique_fields(body: ContactModel, db: Session) -> Contact|None:
    return db.query(Contact).filter(or_(Contact.phone==body.phone, Contact.email==body.email)).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(**body.model_dump())

    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    return contact


async def update_contact(body: ContactModel, contact_id: int, db: Session) -> Contact|None: 
    contact = await get_contact_by_id(contact_id, db)
    
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.description = body.description

        db.commit()

    return contact


async def delete_contact(contact_id: int, db: Session) -> Contact:
    contact = await get_contact_by_id(contact_id, db)
    
    if contact:
        db.delete(contact)
        db.commit()

    return contact


async def get_upcoming_birthdays(db: Session) -> List[Contact]:
    result = []
    
    start_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    list_date = []
    
    count = 1
    while count <= 7:
        start_date += timedelta(1)
        list_date.append(start_date)
        count += 1
    
    contacts = db.query(Contact).all()

    for date in list_date:
        for contact in contacts:
            if contact.birthday.month == date.month and contact.birthday.day == date.day:
                result.append(contact)
                break
    
    return result
