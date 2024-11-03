"""cria relacionamento entre cliente e pedido 

Revision ID: 029169bec9c5
Revises: a256e364cb7b
Create Date: 2024-11-03 14:11:54.201946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '029169bec9c5'
down_revision: Union[str, None] = 'a256e364cb7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Cria a coluna cliente_id em pedidos e estabelece chave estrangeira para clientes.id
    op.add_column('pedidos', sa.Column('cliente_id', sa.Integer(), sa.ForeignKey('clientes.id'), nullable=False))

def downgrade() -> None:
    # Remove a coluna cliente_id de pedidos caso a migração seja revertida
    op.drop_column('pedidos', 'cliente_id')
