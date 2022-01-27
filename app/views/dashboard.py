from flask import Blueprint, render_template, make_response
from neo4j_service import Neo4jService

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/home')
def home():
    """
    Render the home page for the 'dashboard' module
    This returns the names and URLs of adjacent directories
    """
    return render_template("register.html", tagname = 'home')

@dashboard.route('/links/<setup>')
def setup_links(setup):
    """
    Render the home page for the 'dashboard' module
    This returns the names and URLs of adjacent directories
    """
    nsrv_obj = Neo4jService()
    all_setups = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) RETURN m", {})
    setups_json = all_setups.data()
    setups_labels = [list(node['m'].labels)[0] for node in setups_json]
    # [{'m': Node('home_setup', setup=True)}, {'m': Node('home_setup', setup=True)}]
    return render_template("links.html", tagname = 'links', setup = setup, setup_labels = set(setups_labels))

@dashboard.route('/links')
def links():
    """
    Render the home page for the 'dashboard' module
    This returns the names and URLs of adjacent directories
    """
    nsrv_obj = Neo4jService()
    all_setups = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) RETURN m", {})
    setups_json = all_setups.data()
    setups_labels = [list(node['m'].labels)[0] for node in setups_json]
    # [{'m': Node('home_setup', setup=True)}, {'m': Node('home_setup', setup=True)}]
    return render_template("links.html", tagname = 'links', setup = setups_labels[0] if setups_labels else "", setup_labels = set(setups_labels))

@dashboard.route('/delete/<setup>')
def delete_setup(setup):
    """
    Render the thing description deletion page for the 'dashboard' module
    """
    nsrv_obj = Neo4jService()
    all_setups = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) RETURN m", {})
    setups_json = all_setups.data()
    setups_labels = list(set([list(node['m'].labels)[0] for node in setups_json]))
    nodes = list()
    if setups_labels:
        nodes = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) where m.name=$setup RETURN n", {"setup":setup}).data()
    clean_nodes = [node['n'] for node in nodes]
    return render_template("delete.html", tagname = 'delete', setup = setup, setup_nodes = clean_nodes, setups_labels = setups_labels)

@dashboard.route('/delete')
def delete():
    """
    Render the thing description deletion page for the 'dashboard' module
    """
    nsrv_obj = Neo4jService()
    all_setups = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) RETURN m", {})
    setups_json = all_setups.data()
    setups_labels = list(set([list(node['m'].labels)[0] for node in setups_json]))
    # for setup in setups_labels:
    nodes = list()
    if setups_labels:
        nodes = nsrv_obj.run_q("MATCH (n)-[:belongsTo]->(m) where m.name=$setup RETURN n", {"setup":setups_labels[0]}).data()
    clean_nodes = [node['n'] for node in nodes]
    return render_template("delete.html", tagname = 'delete', setup = setups_labels[0] if setups_labels else "", setup_nodes = clean_nodes, setups_labels = setups_labels)

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