from app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get("FLASK_BLOGGER_PORT", 5000))
    app.run(debug=True,port=port)

