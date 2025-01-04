from app.db import crud

mock_data = [
    {
        "query": "What is the capital of France?",
        "context": [
            "France is a country in Western Europe.",
            "The capital city of France is Paris.",
        ],
        "response": "The capital of France is Paris.",
        "document_id": "e22dbf2c-8b4c-47a9-a3fc-dab22c894fec",
        "request_time": "2025-01-04T10:15:30Z",
        "response_time": "2025-01-04T10:15:31Z",
        "duration": 2.15409,
    },
    {
        "query": "Who developed the theory of relativity?",
        "context": [
            "The theory of relativity is a fundamental principle in physics.",
            "Albert Einstein is widely known for his work on the theory of relativity.",
            "Relativity consists of two theories: special relativity and general relativity.",
            "General relativity, published in 1915, explains the gravitational force as a curvature of spacetime.",
            "Einstein's work on relativity has profoundly influenced modern physics and cosmology.",
        ],
        "response": "The theory of relativity was developed by Albert Einstein.",
        "document_id": "a53c61db-75b4-4800-9118-61db56c6dcf0",
        "request_time": "2025-01-04T10:20:45Z",
        "response_time": "2025-01-04T10:20:46Z",
        "duration": 1.98524,
    },
]


# TODO: change this!!
def insert_mock_data():
    data_in_db = list(crud.get_all_documents())
    if data_in_db:
        return None
    crud.insert_documents(mock_data)


insert_mock_data()
