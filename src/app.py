import pandas as pd
from bs4 import BeautifulSoup
import requests
import streamlit as st

st.markdown(
    '''
    <h1 style="padding-left: 10px; padding-bottom: 20px;" align="center">
        Search Engine Scraper
    </h1>
    <p align="right">Built with ☕ by <a href="https://github.com/Kunal-Kumar-Sahoo/" target="_blank">Kunal Kumar Sahoo</a></p>
    ''',
    unsafe_allow_html=True
)

query = st.text_input('', help='Enter the search string and hit Enter/Return')
query = query.replace(' ', '+')
query = query.lower()

if query:
    try:
        req = requests.get(
            f'https://www.bing.com/search?q={query}',
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
            }
        )

        result_str = '<html><table style="border: none;">'

        if req.status_code == 200:
            bs = BeautifulSoup(req.content, features='html.parser')
            search_result = bs.find_all('li', class_='b_algo')
            search_result = [str(i).replace('<strong>', '') for i in search_result]
            search_result = [str(i).replace('</strong>', '') for i in search_result]
            result_df = pd.DataFrame()
            
            for n, i in enumerate(search_result):
                individual_search_result = BeautifulSoup(i, features='html.parser')
                h2 = individual_search_result.find('h2')
                href = h2.find('a').get('href')
                cite = f'{href[:50]}...' if len(href) >= 50 else href
                url_text = h2.find('a').text
                description = '' if individual_search_result.find('p') is None else individual_search_result.find('p').text
                result_df = result_df.append(pd.DataFrame({
                    'Title': url_text,
                    'URL': href,
                    'Description': description
                }, index=[n]))
                count_str = f'<b style="font-size: 20px;">Bing Search returned {len(result_df)} results</b>'

                result_str += f'<tr style="border: none;"><h3><a href="{href}" target="_blank">{url_text}</a></h3></tr>' +\
                    f'<tr style="border: none;"><strong style="color: green;">{cite}</strong></tr>' +\
                    f'<tr style="border: none;">{description}</tr>' +\
                    f'<tr style="border: none;"><td style="border: none;"></td></tr>' 
            
            result_str += '</table></html>'
        
        else:
            print(req.status_code)
            result_df = pd.DataFrame({'Title': '', 'URL': '', 'Description': ''}, index=[0])
            result_str = '<html></html>'
            count_str = '<b style="font-size: 20px;">Looks like an error :(</b>'
    
    except:
        result_df = pd.DataFrame({'Title': '', 'URL': '', 'Description': ''}, index=[0])
        result_str = '<html>From except clause</html>'
        count_str = '<b style="font-size: 20px;">Looks like an error :(</b>'

    try:
        st.markdown(f'{count_str}', unsafe_allow_html=True)
        st.markdown(f'{result_str}', unsafe_allow_html=True)
        st.markdown(f'<h3>Data Frame of the above search result</h3>', unsafe_allow_html=True)
        st.dataframe(result_df)
    except:
        st.markdown(f'<html><h1>Results not found :(</h1></html>', unsafe_allow_html=True)