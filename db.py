#!/usr/bin/env python3
"""DB Module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB():
    """ DB Class """
    def __init__(self) -> None:
        """ Initialize a new DB instance """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ Memorize session object """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, first_name, last_name, email, phone_number, address, hashed_password):
        """add a new user"""
        new_user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, address=address, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> int:
        """ Find USer by """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user:
                return user
            else:
                raise NoResultFound
        except NoResultFound as e:
            raise e
        except InvalidRequestError as err:
            raise err

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update user info """
        try:
            user = self.find_user_by(id=user_id)

            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError

            self._session.commit()

        except ValueError as err:
            raise err
