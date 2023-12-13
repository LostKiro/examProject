import asyncio
import logging
from asyncio import Lock

from PIL import Image, ImageDraw, ImageOps
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6574253125:AAHh1MlYVpQCYlCGdiyAe3NjkI6_bvjSosg")
dp = Dispatcher(bot=bot, storage=MemoryStorage())


@dp.message_handler(text='/start')
async def start(message: types.Message):

    await message.answer(text='Здравствуйте!\nКак Вас зовут?')

# Настройка базы данных
engine = create_engine('sqlite:///bot.db')
Base = declarative_base()

# Определение модели пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))
    email = Column(String(100), unique=True)
    avatar = Column(String(100))  # Путь к файлу аватара пользователя

    def __init__(self, username, password, email, avatar):
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar

Base.metadata.create_all(engine)

# FSM Состояния
class Registration(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
    waiting_for_email = State()
    waiting_for_avatar = State()

db_session = sessionmaker(bind=engine)
session = scoped_session(sessionmaker(bind=engine))

# Регистрация пользователя
@dp.message_handler(commands='register', state='*')
async def register(message: types.Message):
    await Registration.waiting_for_username.set()
    await message.answer("Введите ваш логин:")

@dp.message_handler(state=Registration.waiting_for_username)
async def process_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
    await Registration.next()
    await message.answer("Введите ваш пароль:")

@dp.message_handler(state=Registration.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await Registration.next()
    await message.answer("Введите ваш email:")

@dp.message_handler(state=Registration.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text
    await Registration.next()
    await message.answer("Загрузите вашу аватарку:", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(content_types=['photo'], state=Registration.waiting_for_avatar)
async def process_avatar(message: types.Message, state: FSMContext):
    document_id = message.photo[-1].file_id
    file_info = await bot.get_file(document_id)
    file_path = file_info.file_path
    file = await bot.download_file(file_path)

    async with state.proxy() as data:
        # Сохранение аватара пользователя
        users_avatar_path = 'user_avatars/'

        # Создание круглого аватара с использованием Pillow
        with Image.open(file) as img:
            size = (128, 128)
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)

            img.thumbnail(size)
            output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)

            # Сохраняем аватарку
            avatar_path = f"{users_avatar_path}{message.from_user.id}_avatar.png"
            output.save(avatar_path)

        data['avatar'] = avatar_path
        # Создание нового пользователя и сохранение в БД
        new_user = User(username=data['username'], password=data['password'], email=data['email'], avatar=data['avatar'])
        db = db_session()
        db.add(new_user)
        db.commit()

    await state.finish()
    await message.answer("Вы успешно зарегистрированы!")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    #Base.metadata.create_all(engine)
    asyncio.run(main())
