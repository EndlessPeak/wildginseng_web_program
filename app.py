from App import create_app

app = create_app()

if __name__ == '__main__':
    host = '127.0.0.1'
    app.run(host=host,debug=False)