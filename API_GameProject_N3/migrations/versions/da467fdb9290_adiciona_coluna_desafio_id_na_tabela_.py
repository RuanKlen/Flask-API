"""Adiciona coluna desafio_id na tabela sessao

Revision ID: da467fdb9290
Revises: 1964a4e5b111
Create Date: 2025-06-20 12:17:07.932616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da467fdb9290'
down_revision = '1964a4e5b111'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('insignia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('descricao', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nome')
    )
    with op.batch_alter_table('sessao', schema=None) as batch_op:
        batch_op.add_column(sa.Column('desafio_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_sessao_desafio_id', 'desafio', ['desafio_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sessao', schema=None) as batch_op:
        batch_op.drop_constraint('fk_sessao_desafio_id', type_='foreignkey')
        batch_op.drop_column('desafio_id')

    op.drop_table('insignia')
    # ### end Alembic commands ###
