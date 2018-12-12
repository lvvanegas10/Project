import pandas as pd
import numpy as np
from scipy.spatial import distance_matrix

class DataLoader:

    def __init__(self, fileNumber):
        self.df = pd.read_csv('./PatronesCorte/Temp_GCUT'+str(fileNumber)+'.txt', index_col=False,header=None, sep=r'\t', engine='python')
        self.hash_x = {}
        self.hash_y = {}       
        self.len_coor = 0
        self.coordinates = []
        self.nodes = []
        self.nodes_names = []
        self.nodes_pos = {}

        self.format_data()
        self.init_data()
        self.generate_matrix()
        self.get_travel_time_matrix()
        self.join_matrices()
        self.add_node_names()

    def format_data(self):
        self.size_x = self.df.iloc[0][2]
        self.size_y = self.df.iloc[0][3]
        self.df = self.df.iloc[1:]    
    
        for index, row in self.df.iterrows():
            self.coordinates.append((row[0], row[1]))
            self.coordinates.append((row[0], row[4]))
            self.coordinates.append((row[3], row[4]))
            self.coordinates.append((row[3], row[1]))

        self.coordinates = list(set( self.coordinates))
        self.coordinates_x = sorted( self.coordinates, key=lambda tup: (tup[0], tup[1]))
        self.coordinates_y = sorted( self.coordinates, key=lambda tup: (tup[1], tup[0]))  

    def init_data(self):
        self.len_coor += self.generateNodes(self.coordinates_y,'h','y')
        self.len_coor += self.generateNodes(self.coordinates_x,'v','x')
        
        df_new = pd.DataFrame(self.nodes, columns=['xcord', 'ycord'], index=self.nodes_names)
        self.matrix_d = distance_matrix(df_new.values, df_new.values)
        self.len_matrix = len(self.nodes)//2
        
        self.matrix_ones = np.full((self.len_matrix,self.len_matrix), 9999999999)
        np.fill_diagonal(self.matrix_ones,0)

        self.matrix_ones_a = np.full((self.len_matrix*2,self.len_matrix), 9999999999)
        self.matrix_ones_b = np.full((self.len_matrix,self.len_matrix*2), 9999999999)

    def generateNodes(self, arr, name, coor):
        a = 1
        len_coor = 0
        for i in range(0, len(arr)-1):
            x = arr[i][0]
            y = arr[i][1]
            coor_mov = x if coor == 'x' else y
            coor_mov_n = y if coor == 'x' else x
    
            size = self.size_x if coor == 'x' else self.size_y
            size_n = self.size_y if coor == 'x' else self.size_x

            if(coor_mov_n < size_n  and (coor_mov != 0 and coor_mov != size)):
                x_next = arr[i+1][0]
                y_next = arr[i+1][1]
                coor_n_mov = x_next if coor == 'x' else y_next
                coor_n_mov_n = y_next if coor == 'x' else x_next

                if(coor_n_mov_n == coor_mov_n or coor_n_mov == coor_mov ):
                    self.nodes.append([x,y])
                    self.nodes_names.append(name+str(a)+'a')
                    self.nodes_pos[name+str(a)+'a'] = len(self.nodes) - 1
                    self.nodes.append([x_next,y_next])
                    self.nodes_names.append(name+str(a)+'b')
                    self.nodes_pos[name+str(a)+'b'] = len(self.nodes) - 1
                    len_coor += abs(x-x_next) + abs(y-y_next)
                    a = a + 1
        return len_coor   
        
    def generate_matrix(self):
        aux = 0
        for i in range(0, self.len_matrix*2):
            self.matrix_ones_a[i][aux] = 0
            self.matrix_ones_b[aux][i] = 0
            if(i%2 != 0):
                self.matrix_d[i-1][i] = 0
                aux = aux + 1
            else:
                self.matrix_d[i+1][i] = 0

    def join_matrices(self):
        m1 = np.concatenate((self.matrix_d, self.matrix_ones_a), axis=1)
        m2 = np.concatenate((self.matrix_ones_b, self.matrix_ones), axis=1)
        self.final_matrix = np.concatenate((m1, m2), axis=0)

    def add_node_names(self):
        for i in range(0, len(self.nodes_names), 2):
            name = self.nodes_names[i]
            self.nodes_names.append(name[:2]+'c')
    
    def get_final_matrix(self):
        return self.final_matrix
    
    def get_nodes_names(self):
        return self.nodes_names
    
    def get_cut_time(self):
        return self.time(self.len_coor, True) 

    def get_travel_time_matrix(self):
        time_func = np.vectorize(self.time)
        self.matrix_d = time_func(self.matrix_d, False)
    
    def time(self, dis, bool_Corte): 
        if bool_Corte:
            return (dis*200)
        else:
            if dis<=5:
                return(dis*4000)
            elif dis<=100:
                return(dis*315800+1840000)
            else:
                return(dis*100+40000)
    
    def finalRoute(self, route, num, time, ex_time):    
        points_route = []        
        file = open("./resp/resp"+ str(num) +".txt","w") 
        file.write("Excecution time = " + str(ex_time) + "\n") 
        file.write("Air time = " + str(float(time)/100000) + "\n") 
        file.write("Cut time = " + str(float(self.get_cut_time())/100000) + "\n")
        file.write("Total cut time = " + str((float(self.get_cut_time()) + float(time))/100000) + "\n")
        file.write('['+ str(self.size_x) +  ', '+ str(self.size_y)+']' + '\n') 

        for i in range(0, len(route), 3):
            if(i != len(route)-1):
                pos_1 = self.nodes_pos[route[i]]
                pos_2 = self.nodes_pos[route[i + 2]]   
                points = [self.nodes[pos_1], self.nodes[pos_2]]
                points2 = [self.nodes[pos_2], self.nodes[pos_1]]

                if points not in points_route and points2 not in points_route: 
                    points_route.append(points)
                    file.write(str(self.nodes[pos_1]) + " " + str(self.nodes[pos_2]) + '\n')  
        
        file.close() 



