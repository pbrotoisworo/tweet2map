from src.streamlit import map, plots, home
from src.streamlit.multiapp import MultiApp
    
app = MultiApp()
app.add_app('Home', home.main)
app.add_app('Map', map.main)
app.add_app('Graphs', plots.main)
app.run()