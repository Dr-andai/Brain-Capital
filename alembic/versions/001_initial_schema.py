"""Initial schema with countries, pillars, dimensions, indicators, indicator_values, ai_insights

Revision ID: 001_initial_schema
Revises:
Create Date: 2026-02-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create countries table
    op.create_table(
        'countries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=3), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('region', sa.String(length=100), nullable=True),
        sa.Column('latitude', sa.DECIMAL(precision=9, scale=6), nullable=True),
        sa.Column('longitude', sa.DECIMAL(precision=9, scale=6), nullable=True),
        sa.Column('population', sa.BigInteger(), nullable=True),
        sa.Column('gdp_usd', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code')
    )
    op.create_index('idx_countries_code', 'countries', ['code'])
    op.create_index('idx_countries_region', 'countries', ['region'])

    # Create pillars table
    op.create_table(
        'pillars',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index('idx_pillars_display_order', 'pillars', ['display_order'])

    # Create dimensions table
    op.create_table(
        'dimensions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('pillar_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['pillar_id'], ['pillars.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pillar_id', 'name', name='uq_dimension_pillar_name')
    )
    op.create_index('idx_dimensions_pillar_id', 'dimensions', ['pillar_id'])
    op.create_index('idx_dimensions_display_order', 'dimensions', ['display_order'])

    # Create indicators table
    op.create_table(
        'indicators',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dimension_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('unit', sa.String(length=100), nullable=True),
        sa.Column('data_source', sa.String(length=255), nullable=True),
        sa.Column('methodology_url', sa.Text(), nullable=True),
        sa.Column('display_order', sa.Integer(), server_default='0', nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['dimension_id'], ['dimensions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('dimension_id', 'name', name='uq_indicator_dimension_name')
    )
    op.create_index('idx_indicators_dimension_id', 'indicators', ['dimension_id'])
    op.create_index('idx_indicators_is_active', 'indicators', ['is_active'])
    op.create_index('idx_indicators_display_order', 'indicators', ['display_order'])

    # Create indicator_values table
    op.create_table(
        'indicator_values',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('country_id', sa.Integer(), nullable=False),
        sa.Column('indicator_id', sa.Integer(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('value', sa.DECIMAL(precision=15, scale=4), nullable=True),
        sa.Column('confidence_score', sa.DECIMAL(precision=3, scale=2), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['indicator_id'], ['indicators.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('country_id', 'indicator_id', 'year', name='uq_indicator_value')
    )
    op.create_index('idx_indicator_values_country_id', 'indicator_values', ['country_id'])
    op.create_index('idx_indicator_values_indicator_id', 'indicator_values', ['indicator_id'])
    op.create_index('idx_indicator_values_year', 'indicator_values', ['year'])
    op.create_index('idx_indicator_values_composite', 'indicator_values', ['country_id', 'indicator_id', 'year'])

    # Create ai_insights table
    op.create_table(
        'ai_insights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('insight_type', sa.String(length=50), nullable=False),
        sa.Column('country_id', sa.Integer(), nullable=True),
        sa.Column('indicator_id', sa.Integer(), nullable=True),
        sa.Column('pillar_id', sa.Integer(), nullable=True),
        sa.Column('dimension_id', sa.Integer(), nullable=True),
        sa.Column('year_start', sa.Integer(), nullable=True),
        sa.Column('year_end', sa.Integer(), nullable=True),
        sa.Column('filter_params', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('insight_text', sa.Text(), nullable=False),
        sa.Column('confidence_score', sa.DECIMAL(precision=3, scale=2), nullable=True),
        sa.Column('model_version', sa.String(length=100), nullable=True),
        sa.Column('generated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('user_feedback', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['indicator_id'], ['indicators.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['pillar_id'], ['pillars.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['dimension_id'], ['dimensions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_ai_insights_insight_type', 'ai_insights', ['insight_type'])
    op.create_index('idx_ai_insights_country_id', 'ai_insights', ['country_id'])
    op.create_index('idx_ai_insights_indicator_id', 'ai_insights', ['indicator_id'])
    op.create_index('idx_ai_insights_generated_at', 'ai_insights', ['generated_at'])
    op.create_index('idx_ai_insights_filter_params', 'ai_insights', ['filter_params'], postgresql_using='gin')


def downgrade() -> None:
    op.drop_table('ai_insights')
    op.drop_table('indicator_values')
    op.drop_table('indicators')
    op.drop_table('dimensions')
    op.drop_table('pillars')
    op.drop_table('countries')
