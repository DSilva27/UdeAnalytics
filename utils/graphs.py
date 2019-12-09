import networkx as nx
import matplotlib.pyplot as plt
import data_parser

def make_graph(file_pahts, directed=True):
    ''' Graph builder. File_path is a tuple: (following_paht, followers_path) '''
    
    # load de data from the text files
    j_following = data_parser.parse_from_txt(file_paths[0])
    j_followers = data_parser.parse_from_txt(file_paths[1])

    # collect the user id's from the data
    users = [dic["user_id"] for dic in j_followers]

    # makes a directed grpah if the directed option is True, makes a normal graph otherwise
    if directed:
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    # adds the user nodes from the list
    graph.add_nodes_from(users)
    
    # graph building. Iterates over the follower and following list
    for d_follow, d_following in zip(j_followers, j_following):
        for user in users:
            for f_er, f_ing in zip(d_follow["followers"], d_following["following"]):
                
                # if the graph is directed, the conditionals below define the direction of the edge
                if user == f_er and user == f_ing:
                    # if the users follow eachother, the edge is bidirectional
                    graph.add_edge(d_follow["user_id"], user)
                    graph.add_edge(user, d_follow["user_id"])

                elif user == f_er:
                    graph.add_edge(user, d_follow["user_id"])
                elif user == f_ing:
                    graph.add_edge(d_follow["user_id"], user)

    return graph

def draw_graph(graph, save=False, save_name=None):
    ''' Graph plotter '''
    
    # networkx function to draw the graph on a matplotlib figure
    nx.draw(graph, with_labels=False, font_weight="bold", node_size=10)

    plt.show()

    if save:
        plt.savefig(save_name+".pdf", format="pdf")

if __name__ == "__main__":

    file_paths = ("../data/data_following.json","../data/data_followers.json")

    graph = make_graph(file_paths)
    
    draw_graph(graph)
    
    
