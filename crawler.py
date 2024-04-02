import httplib2
from graph import Graph, dijkstra
from bs4 import BeautifulSoup, SoupStrainer
from urllib.parse import urlparse
from visualize_graph import draw_graph


def get_absolute_links_from_other_domain_only_domains(url):
    try:
        http = httplib2.Http()
        status, response = http.request(url)
        base_domain = urlparse(url).netloc
        absolute_domains = set()  # Usamos un conjunto para evitar duplicados
        for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                href = link['href']
                if href.startswith('http://') or href.startswith('https://'):
                    # Parseamos el enlace
                    parsed_href = urlparse(href)
                    # Reconstruimos el enlace solo con el esquema y el dominio
                    base_link = f"{parsed_href.scheme}://{parsed_href.netloc}"
                    if base_link != base_domain:
                        absolute_domains.add(base_link)
        return list(absolute_domains)
    except Exception as e:
        print(f"Error: {e}")
        return []


def graph_of_related_domains(url,recursion_depht):
    current_url = url
    graph = Graph()
    related_domains_to_url = get_absolute_links_from_other_domain_only_domains(url)
    print("Nodo: "+current_url)
    for i in range(len(related_domains_to_url)):
        print("Related domain: " + related_domains_to_url[i])
        graph.add_edge(current_url, related_domains_to_url[i])
    recursive_graph_of_related_domains(graph,related_domains_to_url,recursion_depht,0)
    return graph


def recursive_graph_of_related_domains(graph,list_of_urls,recursion_depht,recursion_counter):
    if recursion_counter < recursion_depht:
        for url in list_of_urls:
            print("Nodo: " + url)
            related_domains_to_url = get_absolute_links_from_other_domain_only_domains(url)
            for i in range(len(related_domains_to_url)):
                print("Related domain: " + related_domains_to_url[i])
                graph.add_edge(url, related_domains_to_url[i])
            recursive_graph_of_related_domains(graph,related_domains_to_url,recursion_depht,recursion_counter+1)


if __name__ == '__main__':
    url_to_scrape = 'http://www.nytimes.com'
    graph = graph_of_related_domains(url_to_scrape,1)
    draw_graph(graph)
    start_node = 'http://www.nytimes.com'
    end_node = 'https://www.linkedin.com'
    shortest_path, shortest_distance = dijkstra(graph, start_node, end_node)
    print("Para llegar desde el dominio ", start_node, "hasta", end_node, "tiene que pasar por las siguientes web:", shortest_path)
    print("El coeficiente de relación es:", shortest_distance)

