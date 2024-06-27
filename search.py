import streamlit as st
import requests
import xml.etree.ElementTree as ET

def fetch_papers(query, max_results):
    base_url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'relevance',
        'sortOrder': 'descending'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        papers = parse_arxiv_response(response.text)
        return papers
    else:
        return None

def parse_arxiv_response(response_text):
    root = ET.fromstring(response_text)
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
        id_url = entry.find('{http://www.w3.org/2005/Atom}id').text
        papers.append({'title': title, 'summary': summary, 'id_url': id_url})
    return papers

def ai_paper_search():
    st.title('AI 논문 검색')
    query = st.text_input('논문 검색어 입력')
    max_results = st.number_input('결과 수', min_value=1, max_value=100, value=10)
    if query:
        st.write(f"'{query}'에 대한 논문 검색 결과를 표시합니다.")
        papers = fetch_papers(query, max_results)
        if papers:
            for paper in papers:
                st.subheader(paper['title'])
                st.write(paper['summary'])
                st.write(f"[DOI 링크]({paper['id_url']})")
        else:
            st.write("검색 결과가 없습니다.")

if __name__ == "__main__":
    ai_paper_search()
