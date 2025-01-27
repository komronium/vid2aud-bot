from datetime import date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, func
from config import settings
from app.models.user import User, engine


class UserService:
    def __init__(self):
        self.channel_usernmae = settings.CHANNEL_USERNAME
        self.Session = sessionmaker(bind=engine)

    async def get_users(self):
        session = self.Session()
        users = session.query(User).all()
        return users

    async def get_user_count(self):
      session = self.Session()
      count = session.query(User).count()
      return count

    async def get_today_joined_user_count(self):
        session = self.Session()
        users = session.query(User).filter(User.joined_date == date.today())
        return users.count()

    async def get_top_5_user(self):
        session = self.Session()
        users = session.query(User).order_by(text('-conversion_count')).limit(5)
        return users

    async def get_conversion_count(self):
        session = self.Session()
        count = session.query(func.sum(User.conversion_count)).scalar()
        return count

    async def add_conversion(self, user_id):
        session = self.Session()
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            user.conversion_count += 1
            session.commit()

    async def add_user(self, user):
        session = self.Session()
        try:
            existing_user = session.query(User).filter(User.user_id == user.id).first()
            if not existing_user:
                new_user = User(
                    user_id=user.id,
                    username=user.username,
                    full_name=f"{user.first_name} {user.last_name if user.last_name else ''}"
                )
                session.add(new_user)
                session.commit()

                from app.utils.notify_group import notify_group_about_new_user
                await notify_group_about_new_user(user.bot, user)
        except Exception as e:
            print(f"Error adding user to database: {e}")
        finally:
            session.close()

