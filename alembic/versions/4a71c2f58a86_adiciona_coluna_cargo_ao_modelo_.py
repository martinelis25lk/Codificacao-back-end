from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4a71c2f58a86'
down_revision = '5300552b09e7'
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona a nova coluna 'cargo' à tabela 'users'
    op.add_column('users', sa.Column('cargo', sa.String(), nullable=False, server_default='usuario'))


def downgrade():
    # Remove a coluna 'cargo' caso a migração seja revertida
    op.drop_column('users', 'cargo')
