import requests

if __name__ == '__main__':
    s = requests.Session()

    r = s.post(
        'http://localhost:8000/login/',
        headers={'username': 'vijay', 'password': 'test'},
    )

    print(f'{r.headers}\n{r.json}')