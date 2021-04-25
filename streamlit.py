from src.streamlit import map
from src.streamlit.multiapp import MultiApp
    
app = MultiApp()
app.add_app("Map", map.main)
# app.add_app("Bar", bar.app)
app.run()