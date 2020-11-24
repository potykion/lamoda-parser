import sqlalchemy as sa
from repka.repositories.aiopg_ import AiopgRepository
from sqlalchemy.dialects.postgresql import ARRAY

from src.clothing.models import Clothing

metadata = sa.MetaData()

clothing_table = sa.Table(
    "clothing",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("type", sa.String),
    sa.Column("images", ARRAY(sa.String)),
    sa.Column("color", sa.String),
)


class ClothingRepo(AiopgRepository[Clothing]):
    """Репо для работы со шмотками"""

    table = clothing_table
