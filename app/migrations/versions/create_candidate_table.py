"""create candidate table

Revision ID: create_candidate_table
Revises: 
Create Date: 2024-04-04 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_candidate_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('candidate',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('cv_text', sa.Text(), nullable=False),
        sa.Column('analysis', sa.Text(), nullable=True),
        sa.Column('match_score', sa.Float(), nullable=True),
        sa.Column('job_id', sa.Integer(), nullable=False),
        sa.Column('applied_at', sa.DateTime(), nullable=False),
        sa.Column('shortlisted', sa.Boolean(), nullable=True),
        sa.Column('shortlisted_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['job_id'], ['job.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('candidate') 