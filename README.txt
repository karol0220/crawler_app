
aplikacja korzysta z bibliotek: requests, pyaml, elasticsearch, frameworka Flask oraz bazy Elasticsearch 5.5.2 działającej lokalnie


Aplikację uruchamia się wywołując main.py bez żadnych argumentów.


API można uruchomić wywołująć flask_app.py w module api.
API działa lokalnie na porcie 5000.

Przykładowe zapytania:
# zwraca wszystkie obiekty z bazy
GET http://127.0.0.1:5000/get_responses
Headres:
    Identity: sample_user
    Authorization: 114f34c6acc998c38452ecca6967305552b20061

# zwraca obiekty dla domeny wp.pl
GET http://127.0.0.1:5000/get_responses/wp.pl
Headres:
    Identity: sample_user
    Authorization: 1ad7984813a4ffcb9c9f9426ff0dcc9485d45b31

# zwraca obiekty z kodem odpowiedzi 200
GET http://127.0.0.1:5000/get_code_responses/200
Headres:
    Identity: sample_user
    Authorization: 4d1e116b149a13fa3712eb595ce21881ef8f50cf

ilość zwracanych obiektów można ustalić w kwerendach w pliku queries.json


