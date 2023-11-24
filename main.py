from website import create_app
import sys

app = create_app()

if __name__ == '__main__':
    print(sys.version)
    app.run(debug=True)
