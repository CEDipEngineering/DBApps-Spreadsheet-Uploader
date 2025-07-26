import pandera.pandas as pa

files = {
    "Vendas": {
        "schema": pa.DataFrameSchema(
            {
                "data": pa.Column(pa.DateTime, nullable=False),
                "vendedor": pa.Column(str, nullable=False),
                "produto": pa.Column(str, pa.Check.isin(["Paracetamol", "Ibuprofeno", "Tadalafila"]), nullable=False),
                "quantidade": pa.Column(pa.Int64, pa.Check.ge(0), nullable=False),
                "valor": pa.Column(pa.Float, pa.Check.ge(0), nullable=False),
            }
        ),
        "file_name": "vendas",
    }
}