from gevent import monkey

from app.factory import create_app

if __name__ == "__main__":
    monkey.patch_all(thread=False, select=False)
    app = create_app()
    app.run()
