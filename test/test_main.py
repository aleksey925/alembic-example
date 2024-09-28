from unittest.mock import ANY

from sqlalchemy import select

from main import add_warehouse, Warehouse, get_warehouses


async def test_add_warehouse(pg_conn):
    # act
    await add_warehouse(name='Warehouse 1', address='Address 1', conn=pg_conn)

    # assert
    rows = (await pg_conn.execute(select(Warehouse))).all()
    assert len(rows) == 1
    assert rows[0].name == 'Warehouse 1'
    assert rows[0].address == 'Address 1'


async def test_get_warehouses(pg_conn):
    # arrange
    await add_warehouse(name='Warehouse 1', address='Address 1', conn=pg_conn)
    await add_warehouse(name='Warehouse 3', address='Address 3', conn=pg_conn)

    # act
    result = await get_warehouses(conn=pg_conn)

    # assert
    assert len(result) == 2
    assert result == [
        {'address': 'Address 1', 'id': ANY, 'name': 'Warehouse 1'},
        {'address': 'Address 3', 'id': ANY, 'name': 'Warehouse 3'}
    ]
