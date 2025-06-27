import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine, engine

from api.config import MYSQL_ACCOUNT, MYSQL_HOST, MYSQL_PASSWORD, MYSQL_PORT


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = f"mysql+pymysql://{MYSQL_ACCOUNT}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/mydb"

    # 建立 SQLAlchemy 引擎物件
    engine = create_engine(address)
    connect = engine.connect()
    return connect


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/taiwan_stock_price")
def taiwan_stock_price(
    stock_id: str = "",
    start_date: str = "",
    end_date: str = "",
):
    sql = f"""
    select * from taiwan_stock_price
    where StockID = '{stock_id}'
    and Date>= '{start_date}'
    and Date<= '{end_date}'
    """
    mysql_conn = get_mysql_financialdata_conn()
    data_df = pd.read_sql(sql, con=mysql_conn)
    data_dict = data_df.to_dict("records")
    return {"data": data_dict}
