#import necessary libraries for handling json, mathematical operations, matrix multiplication, and os operations
import json
import math
import matmult
import os

#initialize global variable to check if Map_url_to_title_file_name is loaded
is_Map_url_to_title_file_name_loaded = False

#initialize global variable to check if outgoing links are loaded
is_outgoing_links_loaded = False
#initialize dictionary to store outgoing links
outgoing_links = {}

#initialize global variable to check if incoming links are loaded
is_incoming_links_loaded = False
#initialize dictionary to store incoming links
incoming_links = {}

#initialize global variable to check if idf values are loaded
is_idf_values_loaded = False
#initialize dictionary to store idf values
idf_values = {}

#initialize global variable to check if tf values are loaded
is_tf_values_loaded = False
#initialize dictionary to store tf values
tf_values = {}

#initialize global variable to check if page rank file is exported
is_get_page_rank_file_exported = False
#initialize dictionary to store page rank values
page_rank_values = {}


#retrieves the outgoing links associated with a given URL.
#returns a list or None: A list of outgoing links if found, None otherwise.
def get_outgoing_links(url):
    #declare global variables
    global is_outgoing_links_loaded
    global outgoing_links
    #check if outgoing links are loaded
    if not is_outgoing_links_loaded:
        #open outgoing_links.json file in read mode
        with open("outgoing_links.json","r") as filein:
            #load json data from the file into outgoing_links dictionary
            outgoing_links = json.load(filein)
            #set is_outgoing_links_loaded to True after loading the data
            is_outgoing_links_loaded = True    

    #get the links for the given url from outgoing_links dictionary
    links = outgoing_links.get(url)

    #if no links found, return None
    if not links:
        return None
    #return the links if found
    return links

#retrieves the incoming links with a given URL.
#returns a list or None: A list of incoming links if found, None otherwise.
def get_incoming_links(url):
    #declare global variables
    global is_incoming_links_loaded
    global incoming_links
    #check if incoming links are loaded
    if not is_incoming_links_loaded:
        #open incoming_links.json file in read mode
        with open("incoming_links.json","r") as filein:
            #load json data from the file into incoming_links dictionary
            incoming_links = json.load(filein)
            #set is_incoming_links_loaded to True after loading the data
            is_incoming_links_loaded = True    

    #get the links for the given url from incoming_links dictionary
    links = incoming_links.get(url)

    #if no links found, return None
    if not links:
        return None
    #return the links if found
    return links


#🎆custom function
#function goal:
#the generate_probability_matrix function is used to generate a probability matrix 
#based on the given alpha value. This matrix is used in the getPageRank algorithm.
#inputs:
#the function takes one input: alpha. this is a float value used to calculate the probability matrix.
#outputs:
#the function returns a 2D list representing the probability matrix. The matrix is used in the 
#getPageRank algorithm to determine the importance of different pages.
def generate_probability_matrix(alpha):
    #open Map_url_to_title_file_name.json file in read mode
    with open("Map_url_to_title_file_name.json","r") as filein:
        #load json data from the file into Map_url_to_title_file_name dictionary
        Map_url_to_title_file_name = json.load(filein)
    #generate adjacency matrix
    urls = list(Map_url_to_title_file_name)
    N = len(urls)
    matrix = []
    
    #iterate over the range of N
    for i in range(N):
        row = []
        #iterate over the range of N
        for j in range(N):
            #check if urls[j] is in get_outgoing_links(urls[i])
            if urls[j] in get_outgoing_links(urls[i]):
                #append 1 to row
                row.append(1)
            else:
                #append 0 to row
                row.append(0)
        #append row to matrix
        matrix.append(row)
    
    #normalize rows with no 1s
    for row in matrix:
        #check if the row has no 1s
        if sum(row) == 0:
            #iterate over the range of N
            for j in range(N):
                #set row[j] to 1/N
                row[j] = 1/N
    
    #normalize rows with 1s
    for row in matrix:
        #count the number of 1s in row
        count_ones = row.count(1)
        #check if the row has any 1s
        if count_ones > 0:
            #iterate over the length of row
            for j in range(len(row)):
                #check if row[j] is 1
                if row[j] == 1:
                    #set row[j] to 1/count_ones
                    row[j] = 1/count_ones
    
    #multiply the matrix by (1- 𝝰)
    for i in range(N):
        for j in range(N):
            matrix[i][j] *= (1 - alpha)
    
    #add 𝝰/N to each entry of the matrix
    for i in range(N):
        for j in range(N):
            matrix[i][j] += alpha/N
    
    #return the matrix
    return matrix


#🎆custom function
#function Goal:
#the initialize_page_rank_vector function is used to initialize a PageRank vector 
#based on the given matrix. 
#inputs:
#the function takes one input: matrix, This represents the probability matrix. 
#outputs:
#the function returns a 2D list representing the initial PageRank vector which is π0. Each element 
#in this vector is initialized to 1/N, where N is the number of pages in the 
#probability matrix. 
def initialize_page_rank_vector(matrix):
    #get the number of columns in the matrix
    N = len(matrix[0])
    #initialize matrix with 1/N
    page_rank_vector = [[1/N]*N]
    #return the page rank vector
    return page_rank_vector



#🎆custom function
#function goal:
#the calculate_page_rank function is used to calculate the PageRank of a given matrix 
#using an iterative method.
#inputs:
#the function takes two inputs: 
#1. matrix: This is a 2D list representing the probability matrix used in the getPageRank algorithm.
#2. rank_vector: This is a 2D list representing the initial PageRank vector.
#outputs:
#the function returns a 2D list representing the final rank vector after convergence. 
#This vector represents the PageRank of each page. 
def calculate_page_rank(matrix, rank_vector):
    #set the threshold
    threshold=0.0001
    #get the length of the matrix
    N = len(matrix)
    #set the previous rank vector to the rank vector
    previous_rank_vector = rank_vector
    result = []
    #start an infinite loop
    while True:
        #multiply the rank vector with the probability matrix
        new_rank_vector = matmult.mult_matrix(previous_rank_vector, matrix)
        #if the new and previous rank vectors are the same, break the loop
        if new_rank_vector == previous_rank_vector:
            result = new_rank_vector
            break
        #calculate the Euclidean distance between the new and previous rank vectors
        distance = matmult.euclidean_dist(previous_rank_vector, new_rank_vector)      
        #if the distance is below the threshold, break the loop
        if distance <= threshold:
            result = new_rank_vector
            break
        #update the previous rank vector and the current rank vector
        previous_rank_vector = new_rank_vector

    #return the result
    return result


#🎆custom function
#function goal:
#the store_page_rank_values function uses calculate_page_rank function and 
# stores the PageRank values corresponding to each links 
#in a dictionary. The dictionary is then stored in a JSON file.
#inputs:
#the function takes two inputs: 
#1. matrix: a 2D list representing the probability matrix used in the PageRank algorithm.
#2. rank_vector: a 2D list representing the initial PageRank vector.
#outputs:
#the function does not return any value. Instead, it writes the calculated PageRank values to a 
#JSON file named 'page_rank_values.json'. Each key in the JSON file is a URL, and the 
#corresponding value is the PageRank of that URL.
def store_page_rank_values(matrix, rank_vector):
    #set the threshold
    threshold=0.0001
    #declare global variable
    global page_rank_values

    #open Map_url_to_title_file_name.json file in read mode
    with open("Map_url_to_title_file_name.json","r") as filein:
        #load json data from the file into Map_url_to_title_file_name dictionary
        Map_url_to_title_file_name = json.load(filein)
    #calculate the final rank vector
    final_rank_vector = calculate_page_rank(matrix, rank_vector)

    #get the list of URLs
    urls = list(Map_url_to_title_file_name)

    #assign each PageRank value to its corresponding URL
    for i in range(len(urls)):
        page_rank_values[urls[i]] = final_rank_vector[0][i]

    #store the dictionary into a JSON file
    with open('page_rank_values.json', 'w') as file:
        json.dump(page_rank_values, file)


#retrieves the PageRank value for a given URL.
#returns float: The PageRank value of the URL if it exists in the dictionary, otherwise -1.
def get_page_rank(URL):
    #initialize dictionary to store page rank
    page_rank_dict = {}
    #declare global variable
    global is_get_page_rank_file_exported

    #check if page_rank_values.json file exists
    if ( not(os.path.exists('page_rank_values.json')) ):
        #set is_get_page_rank_file_exported to True
        is_get_page_rank_file_exported = True
        #generate probability matrix
        probability_matrix = generate_probability_matrix(0.1)
        #initialize page rank vector
        page_rank_vector = initialize_page_rank_vector(probability_matrix)
        #store page rank values
        store_page_rank_values(probability_matrix, page_rank_vector)

        #load the PageRank values from the JSON file
        with open('page_rank_values.json', 'r') as file:
            page_rank_dict = json.load(file)

        #check if the URL is in the dictionary
        if URL in page_rank_dict:
            #if the URL is in the dictionary, return its PageRank value
            return page_rank_dict[URL]
        else:
            #if the URL is not in the dictionary, return -1
            return -1

    #check if the URL is not in the dictionary and if the page rank file is not exported
    elif ( (URL not in page_rank_dict) and (not is_get_page_rank_file_exported) ):
        #set is_get_page_rank_file_exported to True
        is_get_page_rank_file_exported = True
        #generate probability matrix
        probability_matrix = generate_probability_matrix(0.1)
        #initialize page rank vector
        page_rank_vector = initialize_page_rank_vector(probability_matrix)
        #store page rank values
        store_page_rank_values(probability_matrix, page_rank_vector)

        #load the PageRank values from the JSON file
        with open('page_rank_values.json', 'r') as file:
            page_rank_dict = json.load(file)

        #check if the URL is in the dictionary
        if URL in page_rank_dict:
            #if the URL is in the dictionary, return its PageRank value
            return page_rank_dict[URL]
        else:
            #if the URL is not in the dictionary, return -1
            return -1
    
    #load the PageRank values from the JSON file
    with open('page_rank_values.json', 'r') as file:
        page_rank_dict = json.load(file)

    #check if the URL is in the dictionary
    if URL in page_rank_dict:
        #if the URL is in the dictionary, return its PageRank value
        return page_rank_dict[URL]
    else:
        #if the URL is not in the dictionary, return -1
        return -1

#get the Inverse Document Frequency (IDF) value for a given word.
#returns int: The IDF value for the given word. If no IDF value is found, 0 is returned.
def get_idf(word):
    #declare global variables
    global is_idf_values_loaded
    global idf_values
    
    #check if idf values are loaded
    if not is_idf_values_loaded:
        #open idf_values.json file in read mode
        with open("idf_values.json", "r") as filein:
            #load json data from the file
            idf_values = json.load(filein)
            #set is_idf_values_loaded to True after loading the data
            is_idf_values_loaded = True

    #get the idf value for the given word from idf_values dictionary
    idf_value = idf_values.get(word)

    #if no idf value found, return 0
    if not idf_value:
        return 0
    #return the idf value if found
    return idf_value

#get the term frequency (tf) value for a given URL and word.
#returns int: The tf value for the given URL and word. Returns 0 if no tf value is found.
def get_tf(url, word):
    #declare global variables
    global is_tf_values_loaded
    global tf_values

    #check if tf values are loaded
    if not is_tf_values_loaded:
        #open tf_values.json file in read mode
        with open("tf_values.json", "r") as filein:
            #load json data from the file into tf_values dictionary
            tf_values = json.load(filein)
            #set is_tf_values_loaded to True after loading the data
            is_tf_values_loaded = True

    #get the tf value for the given url and word from tf_values dictionary
    tf_value = tf_values.get(str(url+" "+word))

    #if no tf value found, return 0
    if not tf_value:
        return 0
    #return the tf value if found
    return tf_value


#calculate the tf-idf value for a given URL and word.
#returns float: The tf-idf value for the given URL and word.
def get_tf_idf(URL, word):
    #return the tf-idf value calculated using the formula
    return math.log2(1 + get_tf(URL, word))*get_idf(word)