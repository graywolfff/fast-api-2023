from fastapi import APIRouter, HTTPException, status, Depends
from database.connection import get_session
from sqlmodel import Session, select
from models.events import Event, EventUpdate
from typing import List

event_router = APIRouter(
    tags=['Event']
)


@event_router.get('/', response_model=List[Event])
async def retrieve_all_events(session: Session = Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return events


@event_router.get('/{id}', response_model=Event)
async def retrieve_event(id: int, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Event {} not exist'.format(id)
    )


@event_router.post('/new', status_code=status.HTTP_201_CREATED)
async def create_event(new_event: Event, session: Session = Depends(get_session)) -> Event:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return new_event


@event_router.put('/{id}')
async def update_event(id: int, new_data: EventUpdate, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Event with supplied ID does not exist'
    )


@event_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: int, session: Session = Depends(get_session)):
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Event with supplied ID does not exist'
    )


@event_router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_events(session: Session = Depends(get_session)):
    session.query(Event).delete()
    session.commit()
    return
