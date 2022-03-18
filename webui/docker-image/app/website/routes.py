# APP ROUTES (URLs)

@views.route('/') # Decorator
def home():
    return render_template("home.html", user=current_user)