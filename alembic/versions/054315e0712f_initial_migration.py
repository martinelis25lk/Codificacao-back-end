"""Initial migration

Revision ID: 054315e0712f
Revises: 
Create Date: 2025-01-22 21:32:42.899172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '054315e0712f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ### commands auto gerados pelo Alembic - por favor, ajuste! ###
    op.create_table('produtos',
    sa.Column('codigo', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('descricao', sa.VARCHAR(length=30), nullable=True),
    sa.Column('preco', sa.NUMERIC(precision=10, scale=2), nullable=True),
    sa.Column('data_de_validade', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('categoria', sa.VARCHAR(length=30), nullable=True),
    sa.Column('disponibilidade', sa.BOOLEAN(), nullable=True),
    sa.Column('codigo_de_barras', sa.VARCHAR(length=13), nullable=True),
    sa.Column('secao', sa.VARCHAR(length=30), nullable=True),
    sa.Column('estoque_inicial', sa.INTEGER(), nullable=True),
    sa.Column('imagem', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('codigo', name='produtos_pkey')
    )
    op.create_table('pedidos',
    sa.Column('codigo_pedido', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('periodo', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('status_pedido', sa.BOOLEAN(), nullable=True),
    sa.Column('secao_dos_produtos', sa.VARCHAR(length=45), nullable=True),
    sa.Column('id_do_cliente', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['id_do_cliente'], ['clientes.id'], name='pedidos_id_do_cliente_fkey'),
    sa.PrimaryKeyConstraint('codigo_pedido', name='pedidos_pkey')
    )
    op.create_table('clientes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('cpf', sa.VARCHAR(length=11), nullable=True),
    sa.Column('email', sa.VARCHAR(length=30), nullable=True),
    sa.Column('nome', sa.VARCHAR(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id', name='clientes_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('password', sa.VARCHAR(), nullable=False),
    sa.Column('cargo', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('username', name='users_username_key')
    )
    # ### fim comandos auto gerados ### 






    

def downgrade() -> None:
    op.drop_constraint('pedidos_id_do_cliente_fkey', 'pedidos', type_='foreignkey')  # Remover a constraint
    op.drop_table('clientes')  # Remover a tabela clientes
    op.drop_table('pedidos')   # Remover a tabela pedidos
    op.drop_table('produtos')  # Remover a tabela produtos
    # Adicione o restante das tabelas que você deseja remover
     