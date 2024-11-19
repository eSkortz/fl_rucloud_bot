"""adding m2m tables for orgnizations

Revision ID: 6023ef5ba7d3
Revises: a19b410a3212
Create Date: 2024-11-19 18:43:26.077934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6023ef5ba7d3'
down_revision: Union[str, None] = 'a19b410a3212'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('collaborations_user_id_fkey', 'collaborations', type_='foreignkey')
    op.create_foreign_key(None, 'collaborations', 'users', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('m2m_files_folders_folder_id_fkey', 'm2m_files_folders', type_='foreignkey')
    op.drop_constraint('m2m_files_folders_file_id_fkey', 'm2m_files_folders', type_='foreignkey')
    op.create_foreign_key(None, 'm2m_files_folders', 'files', ['file_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'm2m_files_folders', 'folders', ['folder_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('m2m_users_files_file_id_fkey', 'm2m_users_files', type_='foreignkey')
    op.drop_constraint('m2m_users_files_user_id_fkey', 'm2m_users_files', type_='foreignkey')
    op.create_foreign_key(None, 'm2m_users_files', 'users', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'm2m_users_files', 'files', ['file_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('m2m_users_folders_user_id_fkey', 'm2m_users_folders', type_='foreignkey')
    op.drop_constraint('m2m_users_folders_folder_id_fkey', 'm2m_users_folders', type_='foreignkey')
    op.create_foreign_key(None, 'm2m_users_folders', 'folders', ['folder_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'm2m_users_folders', 'users', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    op.drop_constraint('m2m_users_organizations_organization_id_fkey', 'm2m_users_organizations', type_='foreignkey')
    op.drop_constraint('m2m_users_organizations_user_id_fkey', 'm2m_users_organizations', type_='foreignkey')
    op.create_foreign_key(None, 'm2m_users_organizations', 'organizations', ['organization_id'], ['id'], source_schema='public', referent_schema='public')
    op.create_foreign_key(None, 'm2m_users_organizations', 'users', ['user_id'], ['id'], source_schema='public', referent_schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'm2m_users_organizations', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'm2m_users_organizations', schema='public', type_='foreignkey')
    op.create_foreign_key('m2m_users_organizations_user_id_fkey', 'm2m_users_organizations', 'users', ['user_id'], ['id'])
    op.create_foreign_key('m2m_users_organizations_organization_id_fkey', 'm2m_users_organizations', 'organizations', ['organization_id'], ['id'])
    op.drop_constraint(None, 'm2m_users_folders', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'm2m_users_folders', schema='public', type_='foreignkey')
    op.create_foreign_key('m2m_users_folders_folder_id_fkey', 'm2m_users_folders', 'folders', ['folder_id'], ['id'])
    op.create_foreign_key('m2m_users_folders_user_id_fkey', 'm2m_users_folders', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'm2m_users_files', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'm2m_users_files', schema='public', type_='foreignkey')
    op.create_foreign_key('m2m_users_files_user_id_fkey', 'm2m_users_files', 'users', ['user_id'], ['id'])
    op.create_foreign_key('m2m_users_files_file_id_fkey', 'm2m_users_files', 'files', ['file_id'], ['id'])
    op.drop_constraint(None, 'm2m_files_folders', schema='public', type_='foreignkey')
    op.drop_constraint(None, 'm2m_files_folders', schema='public', type_='foreignkey')
    op.create_foreign_key('m2m_files_folders_file_id_fkey', 'm2m_files_folders', 'files', ['file_id'], ['id'])
    op.create_foreign_key('m2m_files_folders_folder_id_fkey', 'm2m_files_folders', 'folders', ['folder_id'], ['id'])
    op.drop_constraint(None, 'collaborations', schema='public', type_='foreignkey')
    op.create_foreign_key('collaborations_user_id_fkey', 'collaborations', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
