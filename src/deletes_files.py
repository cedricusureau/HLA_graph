import os

def delete_in_folders(path_to_folder, extension):
    for i in os.listdir(path_to_folder):
        if extension in i:
            os.remove(path_to_folder+i)

delete_in_folders("/home/cedric/HLA_graph/result/graph/", ".svg")
delete_in_folders("/home/cedric/HLA_graph/result/html_table/",".html")
delete_in_folders("/home/cedric/HLA_graph/result/html_table_light/",".html")
delete_in_folders("/home/cedric/HLA_graph/result/json/",".json")
delete_in_folders("/home/cedric//HLA_graph/result/raw_data/",".csv")