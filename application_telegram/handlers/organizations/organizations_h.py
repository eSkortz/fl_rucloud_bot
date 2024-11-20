from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from typing import List
import uuid

from config import database_engine_async, TELEGRAM_TOKEN

from keyboards import delete_message_k, only_to_main_k
from keyboards.organizations import (
    organization_menu_k,
    organizations_file_menu_k,
    organizations_list_k,
    organizations_ls_k,
    confirm_deliting_organization_k,
)
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_organizations_model import Organizations
from database.orm.public_m2m_users_organizations_model import M2M_UsersOrganizations
from database.orm.public_m2m_organizations_folders_model import M2M_OrganizationsFolders
from database.orm.public_m2m_folders_folders_model import M2M_FoldersFolders
from database.orm.public_m2m_files_folders_model import M2M_FilesFolders
from database.orm.public_folders_model import Folders
from database.orm.public_files_model import Files


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=TELEGRAM_TOKEN)


class OrganizationsGroup(StatesGroup):
    waiting_to_name = State()
    waiting_to_user_id = State()


@router.callback_query(F.data == "organizations_list")
async def organizations_list(callback: CallbackQuery) -> None:
    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == callback.message.chat.id],
        get_unpacked=True,
    )
    organizations_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_UsersOrganizations.organization_id,
        where_params=[M2M_UsersOrganizations.user_id == user.id],
    )
    organizations: List[Organizations] = await database_worker.custom_orm_select(
        cls_from=Organizations, where_params=[Organizations.id.in_(organizations_ids)]
    )

    markup_inline = organizations_list_k.get(organizations=organizations)
    await callback.message.delete()
    await callback.message.answer(
        text=f">🏣 Список всех доступных организаций",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("organization_menu"))
async def organization_menu(callback: CallbackQuery) -> None:
    organization_id = int(callback.data.split("|")[1])

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == callback.message.chat.id],
        get_unpacked=True,
    )
    organization: Organizations = await database_worker.custom_orm_select(
        cls_from=Organizations,
        where_params=[Organizations.id == organization_id],
        get_unpacked=True,
    )

    markup_inline = organization_menu_k.get(
        organization=organization,
        is_owner=True if organization.user_id == user.id else False,
    )
    await callback.message.delete()
    await callback.message.answer(
        text=f">🏣 {organization.name}",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("organizations_ls"))
async def organizations_ls(callback: CallbackQuery) -> None:
    current_folder_id: int = int(callback.data.split("|")[1])
    current_organization_id: int = int(callback.data.split("|")[2])

    current_organization: Organizations = await database_worker.custom_orm_select(
        cls_from=Organizations,
        where_params=[Organizations.id == current_organization_id],
        get_unpacked=True,
    )

    if current_folder_id:
        current_folder: Folders = await database_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.id == current_folder_id],
            get_unpacked=True,
        )
        parent_folder: Folders = await database_worker.custom_orm_select(
            cls_from=M2M_FoldersFolders,
            where_params=[M2M_FoldersFolders.child_folder_id == current_folder.id],
            get_unpacked=True,
        )
        fallback_string = (
            f"organizations_ls|{parent_folder.id}|{current_organization_id}"
        )
    else:
        root_folder_id: Folders = await database_worker.custom_orm_select(
            cls_from=M2M_OrganizationsFolders.folder_id,
            where_params=[
                M2M_OrganizationsFolders.organization_id == current_organization_id,
                M2M_OrganizationsFolders.is_root == True,
            ],
            get_unpacked=True,
        )
        current_folder: Folders = await database_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.id == root_folder_id],
            get_unpacked=True,
        )
        fallback_string = "organizations_list"

    child_folders_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_FoldersFolders,
        where_params=[M2M_FoldersFolders.parent_folder_id == current_folder.id],
    )
    child_folders: List[Folders] = await database_worker.custom_orm_select(
        cls_from=Folders, where_params=[Folders.id.in_(child_folders_ids)]
    )

    inner_files_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_FilesFolders,
        where_params=[M2M_FilesFolders.folder_id == current_folder.id],
    )
    inner_files: List[Files] = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id.in_(inner_files_ids)]
    )

    markup_inline = organizations_ls_k.get(
        folders=child_folders,
        files=inner_files,
        current_folder=current_folder,
        fallback_string=fallback_string,
        organization_id=current_organization_id,
    )
    await callback.message.delete()
    await callback.message.answer(
        text=f">🏣 {current_organization.name} | {current_folder.name if current_folder_id else 'Main Folder'}",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("organizations_file_menu"))
async def organizations_file_menu(callback: CallbackQuery) -> None:
    current_file_id: int = int(callback.data.split("|")[1])
    current_organization_id: int = int(callback.data.split("|")[2])

    current_file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id == current_file_id]
    )
    parent_folder_id: int = await database_worker.custom_orm_select(
        cls_from=M2M_FilesFolders.folder_id,
        where_params=[M2M_FilesFolders.file_id == current_file_id],
        get_unpacked=True,
    )
    parent_folder: Folders = await database_worker.custom_orm_select(
        cls_from=Folders,
        where_params=[Folders.id == parent_folder_id],
        get_unpacked=True,
    )

    markup_inline = organizations_file_menu_k.get(
        file=current_file,
        fallback_string=f"organizations_ls|{parent_folder.id}|{current_organization_id}",
    )
    await callback.message.delete()
    await callback.message.answer(
        text=f">📑 {current_file.name}",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


# create_organization
@router.callback_query(F.data.startswith("create_organization"))
async def get_name(callback: CallbackQuery, state: FSMContext) -> None:
    sent_message = await callback.message.answer(text="Введите имя для новой организации")
    await state.set_state(OrganizationsGroup.waiting_to_name)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)

@router.message(OrganizationsGroup.waiting_to_name)
async def process_organization_name(message: Message, state: FSMContext):
    organization_name = message.text
    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    id_deleted = False
    data_to_insert = {
        "user_id": message.chat.id,
        "name": organization_name,
        "is_deleted": id_deleted
    }

    await database_worker.custom_insert(cls_to=Organizations, data=[data_to_insert])

    sent_message = await callback.message.answer(text="Введите никнеймы пользователей, которых вы желаете добавить")
    await state.set_state(OrganizationsGroup.waiting_to_user_id)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(organization_name=organization_name)

@router.message(OrganizationsGroup.waiting_to_user_id)
async def process_users(message: Message, state: FSMContext):
    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]
    organization_name = state_data["organization_name"]
    users_name = message.text.split(",")

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    organization: Organizations = database_worker.custom_orm_select(
        cls_from=Organizations,
        where_params=[Organizations.name == organization_name],
        get_unpacked=True,
    )

    for user in users_name:
        user_from_db: Users = await database_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == user],
            get_unpacked=True,
        )

        data_to_insert = {
            "user_id": user_from_db.id,
            "organization_id": organization.id,
        }

        await database_worker.custom_insert(cls_to=M2M_UsersOrganizations, data=[data_to_insert])

    markup_inline = only_to_main_k.get()
    await callback.message.answer(
        text=f"Организация успешно создана",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


# share_organization
@router.callback_query(F.data.startswith("share_organization"))
async def share_organization(callback: CallbackQuery) -> None:
    markup_inline = only_to_main_k.get()
    await callback.message.answer(
        text=f"Пользователи успешно добавлены",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )

# delete_organization
@router.callback_query(F.data.startswith("delete_organization"))
async def delete_organization(callback: CallbackQuery) -> None:
    id_to_delete= int(callback.data.split("|")[1])

    await database_worker.custom_delete_all(
        cls_from=Organizations,
        where_params=[Folders.id == id_to_delete],
    )

    await callback.message.delete()

    markup_inline = only_to_main_k.get()
    await callback.message.answer(
        text=f"Организация успешно удалена",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
# ok_delete_organization
