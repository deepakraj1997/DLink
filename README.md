This is the home of project "DLink" - Graphical Representation of Linked Features.

Requirements before running the application:

Download neo4j desktop: https://neo4j.com/download/

Once you have downloaded these, open the neo4j desktop app and click on new project. This will create a new project and this will be your project hosting your database. You can then create a database or start a database from the menu which will then start a database listening on http://localhost:7474/browser/

Go to the http://localhost:7474/browser/ and type in your credentials which you have setup when you are creating the database. This will give you the CLI to the neo4j graph.


Once the above is setup, go to `app/template/links.html` and change the user name and password to what you have setup in the above. 

      server_url: "bolt://localhost:7687",
      server_user: "xxxxxxx",
      server_password: "xxxxxxx",

You might want to change the password and user in `app/neo4j_service.py` and `config/config.ini`.

Once the above is done, do a `pip install -r requirements.txt` under app directory. 
Start the app by running `python3 app.py`

For registration of thing. Use the home setup directory under linked_features. Remember that you need to register the dependency first before the actual node. 

The order of registration:

- zone.json
- kitchen.json
- livingroom.json
- wifi.json
- tab.json
- smarthomecontroller
- cam
- lightsystem
- plug1, plug2
- light1, light2
