import requests

url = "http://localhost:8000/api/chart"
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImIyNDg2Mzc0OTVjYjM4N2U0OWViNmRlMThkZjk5N2VlOGU1YWUyOTciLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiU29jaWFsQWNjb3VudC1JIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0lpVXBwYWxpNzZTVE1WeEwwU2gzb3ZaVFFsakRoMDU0NUpiVThoWmVOZFp1bzZ3UT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9hc3Ryb3N1dHJhYWktYjUyNGUiLCJhdWQiOiJhc3Ryb3N1dHJhYWktYjUyNGUiLCJhdXRoX3RpbWUiOjE3ODQ4MDUxNTcsInVzZXJfaWQiOiJrdTNkUkpHWWFXU29sdVZZWExiYWdPT1RveDkyIiwic3ViIjoia3UzZFJKR1lhV1NvbHVWWVhMYmFnT09Ub3g5MiIsImlhdCI6MTc4NDgwNTE1NywiZXhwIjoxNzg0ODA4NzU3LCJlbWFpbCI6ImNhcmVlcnRyYWNrZXIuc29jaWFsMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNzEwNTk0MDk0MDA2Nzk4NjQzMyJdLCJlbWFpbCI6WyJjYXJlZXJ0cmFja2VyLnNvY2lhbDFAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoiZ29vZ2xlLmNvbSJ9fQ.mToCKQvTetR-6gZbrhg1N9pNNOeTrSD0jgZ0qkFynyxSqcllkSKw5du5z2iugluK28KLMBY_9WDL59oWyHj8a9Ga6juR4XItxlJEFDy7Ktkc67op8xj-_t2sCzt_zvqxH17SfawadGH_dzq6VVR85-LM3RxuRzRXlGed-A4_8D85pjuY4iN62JRF7dl2Dm9M1ewodeAslTl1suXkcTNUwm4S8dXAMhH5QPT6oOKMfyoI0_LGUG730WF2aL61Ew1ggzX9wLD2qwz31-_jfz0mOruUNAPrzNJvwE9vQcuyb-tNKrxVGrF9x7h7Qgt3pzUU0wS-RHbjTp1tAo-yBLUVSg"

payload = {
    "name": "SocialAccount-I",
    "date_str": "2000-01-01",
    "time_str": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "session_id": "test_session_id_999",
    "mode": "exact"
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

try:
    res = requests.post(url, json=payload, headers=headers, timeout=10)
    print("Status:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Request failed:", e)
