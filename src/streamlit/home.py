import streamlit as st

def main():
    
    st.title('Tweet2Map Data Explorer')
    st.markdown("""
            
            The Tweet2Map Data Explorer allows users to easily navigate the traffic incident database.
            
            Tweet2Map is a semi-automated process of getting traffic incident Tweets from the Metro Manila Development Authority (MMDA)
            and then parsing the information into a usable database. I will be building a database over time and sharing the output with
            everyone.
            
            [View the source code on the Github](https://github.com/pbrotoisworo/tweet2map)
            
            **Disclaimer**: There may be some errors and some gaps related to the acquisition and parsing of the Twitter data but most of
            it should be accurate. Read more about MMDA Tweet2Map code on this blog post.
            
            This web app is a work in progress.
            
            Last updated on April 26, 2021.
            """)
    