import json
from chatx.genie_result import GenieResult
from databricks.sdk.service.sql import (
    StatementResponse,
    ColumnInfoTypeName,
    ResultData,
    ResultManifest,
    ResultSchema,
    ColumnInfo,
)
from databricks.sdk.service.dashboards import GenieResultMetadata


def test_genie_result() -> None:
    result = GenieResult(
        query_description="Test Query",
        query_result_metadata=GenieResultMetadata(row_count=5),
        statement_response=StatementResponse(
            result=ResultData(
                data_array=[
                    [1, "Alice", 100.0],
                    [2, "Bob", 200.0],
                    [3, "Charlie", 300.0],
                ]
            ),
            manifest=ResultManifest(
                schema=ResultSchema(
                    columns=[
                        ColumnInfo(name="id", type_name=ColumnInfoTypeName.INT),
                        ColumnInfo(name="name", type_name=ColumnInfoTypeName.STRING),
                        ColumnInfo(name="amount", type_name=ColumnInfoTypeName.DOUBLE),
                    ]
                )
            ),
        ),
    )
    response = json.dumps(result.process_query_results().as_dict())
    
    assert "1" in response
    assert "Alice" in response
    assert "100.00" in response
    assert "2" in response
    assert "Bob" in response
    assert "200.00" in response  

    assert "**Row Count:** 5" in response
      
