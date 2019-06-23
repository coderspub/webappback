from bse_fleet import app as f_app
#uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:f_app

if __name__=="__main__":
    f_app.run()
