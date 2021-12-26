from flask import Blueprint, render_template

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/home')
def home():
    """
    Render the home page for the 'dashboard' module
    This returns the names and URLs of adjacent directories
    """
    return render_template("register.html", tagname = 'home')

@dashboard.route('/links')
def links():
    """
    Render the home page for the 'dashboard' module
    This returns the names and URLs of adjacent directories
    """
    return render_template("links.html", tagname = 'links')

@dashboard.route('/delete')
def delete():
    """
    Render the thing description deletion page for the 'dashboard' module
    """
    return render_template("delete.html", tagname = 'delete')

@dashboard.route('/register')
def register():
    """
    Render the thing description register page for the 'dashboard' module
    """
    return render_template('register.html', tagname = 'register')

# @dashboard.route('/policy')
# def policy():
#     """
#     Render the policy page for the 'dashboard' module
#     """
#     return render_template('policy.html', tagname = 'policy')