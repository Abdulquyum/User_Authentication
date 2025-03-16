#!/usr/bin/env python3
""" Auth file """

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


class Auth:
    """Auth class to interact with the authentication database"""

    def __init__(self):
        """imported db class"""
        self._db = DB()

    def register_user(self, first_name, last_name, email, phone_number, address, password) -> User:
        """help register method"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exist")

        except NoResultFound as err:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(first_name, last_name, email, phone_number, address, hashed_password)

            return new_user

    def valid_login(self, email, password) -> bool:
        """Check if user exist"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email) -> str:
        """create session """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

            return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user By session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy user session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except NoResultFound:
            return None

    @staticmethod
    def _generate_uuid() -> str:
        """generate uuid for user"""
        return str(uuid.uuid4())

    @staticmethod
    def _hash_password(password: str) -> bytes:
        """Hash password """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return hashed_password

