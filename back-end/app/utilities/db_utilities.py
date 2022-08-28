def table_data_to_dict(table_data):
    organised_data = []
    if isinstance(table_data, list):
        for row in table_data:
            organised_data.append({col.name: getattr(row, col.name) for col in row.__table__.columns})
    else:
        return table_data
    return organised_data