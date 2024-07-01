"""db_v01

Revision ID: d7b709000190
Revises: 
Create Date: 2024-06-30 18:58:22.551240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7b709000190'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('genre', sa.String(), nullable=True),
    sa.Column('summary', sa.String(), nullable=True),
    sa.Column('year_published', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_books_author'), 'books', ['author'], unique=False)
    op.create_index(op.f('ix_books_genre'), 'books', ['genre'], unique=False)
    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=True)
    op.create_index(op.f('ix_books_summary'), 'books', ['summary'], unique=False)
    op.create_index(op.f('ix_books_title'), 'books', ['title'], unique=True)
    op.create_index(op.f('ix_books_year_published'), 'books', ['year_published'], unique=False)
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('review_text', sa.String(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reviews_book_id'), 'reviews', ['book_id'], unique=False)
    op.create_index(op.f('ix_reviews_id'), 'reviews', ['id'], unique=True)
    op.create_index(op.f('ix_reviews_rating'), 'reviews', ['rating'], unique=False)
    op.create_index(op.f('ix_reviews_review_text'), 'reviews', ['review_text'], unique=False)
    op.create_index(op.f('ix_reviews_user_id'), 'reviews', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reviews_user_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_review_text'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_rating'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_book_id'), table_name='reviews')
    op.drop_table('reviews')
    op.drop_index(op.f('ix_books_year_published'), table_name='books')
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_index(op.f('ix_books_summary'), table_name='books')
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.drop_index(op.f('ix_books_genre'), table_name='books')
    op.drop_index(op.f('ix_books_author'), table_name='books')
    op.drop_table('books')
    # ### end Alembic commands ###
