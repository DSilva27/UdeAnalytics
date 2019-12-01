import networkx as nx
import matplotlib.pyplot as plt
import data_parser

def make_graph(file_pahts, directed=True):
    ''' Graph builder. File_path is a tuple: (following_paht, followers_path) '''
    
    j_following = data_parser.parse_from_txt(file_paths[0])
    j_followers = data_parser.parse_from_txt(file_paths[1])

    users = [dic["user_id"] for dic in j_followers]

    if directed:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    for d_follow, d_following in zip(j_followers, j_following):
        for user in users:
            for f_er, f_ing in zip(d_follow["followers"], d_following["following"]):
                if user == f_er and user == f_ing:
                    graph.add_edge(d_follow["user_id"], user)
                    graph.add_edge(user, d_follow["user_id"])

                elif user == f_er:
                    graph.add_edge(user, d_follow["user_id"])
                elif user == f_ing:
                    graph.add_edge(d_follow["user_id"], user)

    return graph

def draw_graph(graph, save=False, save_name=None):
    ''' Graph plotter '''

    plt.subplot(111)
    nx.draw(graph, with_labels=False, font_weight="bold", node_size=10)

    plt.show()

    if save:
        plt.savefig(save_name+".pdf", format="pdf")

if __name__ == "__main__":

    file_paths = ("../data/data_following.json","../data/data_followers.json")

    graph = make_graph(file_paths)

    draw_graph(graph)
    
