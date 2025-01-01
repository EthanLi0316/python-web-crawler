#import necessary modules
import searchdata
import json
import math

#initialize global variables
is_Map_url_to_title_file_name_loaded = False
Map_url_to_title_file_name = {}


#🎆custom function
#function goal:
#vector_square function calculates the square of each element in a vector and sums them up.
#inputs:
#A: a list of numbers representing a vector.
#outputs:
#function returns a single number which is the sum of squares of all elements in the input vector.
def vector_square(A):
    #initialize total to 0
    total = 0
    #initialize counter to 0
    i = 0
    #loop through the vector
    while i < len(A):
        #add the square of each element to total
        total += A[i] ** 2
        #increment counter
        i += 1
    #return the total
    return total


#🎆custom function
#function goal:
#mult_elements_in_vectors function multiplies corresponding elements in two input vectors.
#inputs:
#function takes two inputs: 
#vec1 and vec2: these are lists of numbers representing vectors.
#outputs:
#function returns a list of numbers which are the result of multiplying corresponding elements in the input vectors.
#If the input vectors are not of the same length, function returns None.
def mult_elements_in_vectors(vec1, vec2):
    #check if both vectors have the same length
    if len(vec1) != len(vec2):
        #return None if vectors are not of the same length
        return None
    
    #initialize an empty list to store the result
    result = []
    
    #loop through each element in the vectors
    for i in range(len(vec1)):
        #multiply corresponding elements in vec1 and vec2
        multiplied_value = vec1[i] * vec2[i]
        #append the result to the result list
        result.append(multiplied_value)
    
    #return the result list
    return result


#🎆custom function
#function goal:
#get_search_words_vector function calculates the tf-idf vector for a given phrase.
#inputs:
#function takes one input: 
#phrase: a string representing the search phrase.
#outputs:
#function returns a list of numbers which are the tf-idf values for each word in the input phrase.
def get_search_words_vector(phrase):
    #split the phrase into words
    search_words = phrase.split()
    #initialize a dictionary to store word frequencies
    word_freq = {}
    #initialize a list to store word frequencies
    word_freq_list =[]
    #initialize a list to store idf values
    idf = []
    #loop through each word in the list
    for word in search_words:
        #if the word is already in the dictionary, increment its count
        if word in word_freq:
            word_freq[word] += 1/len(search_words)
        #if the word is not in the dictionary, add it with a count of 1
        else:
            word_freq[word] = 1/len(search_words)
            #append the idf value of the word to the idf list
            idf.append(searchdata.get_idf(word))
    
    #convert the dictionary to a list
    for key in word_freq:
        word_freq_list.append(word_freq[key])
    #calculate tf values
    tf = []
    for x in word_freq_list:
        tf.append(math.log2(1+x))
    #calculate tfidf values
    tfidf = mult_elements_in_vectors(tf,idf)
    #return the tfidf values
    return tfidf


#🎆custom function
#function goal:
#get_docs_vector function calculates tf-idf vector for each text.
#inputs:
#function takes one input: 
#phrase: a string representing search phrase.
#outputs:
#function returns a list of lists. each inner list represents a text and 
#contains tf-idf values for each word in input phrase and text's url.
def get_docs_vector(phrase):
    #access the global variable
    global Map_url_to_title_file_name

    #check if the map of url to title file name is loaded
    if not is_Map_url_to_title_file_name_loaded:
        #if not, load the map from the json file
        with open("Map_url_to_title_file_name.json","r") as filein:
            Map_url_to_title_file_name = json.load(filein)
    
    #split the phrase into words and remove leading and trailing spaces
    search_words = phrase.strip().split()
    #initialize a list to store unique words
    unique_words = []
    #initialize a list to store search words vector
    docs_vector = []

    #loop through each word in the search words
    for word in search_words:
        #if the word is not in the unique words list, add it
        if word not in unique_words:
            unique_words.append(word)       
    #loop through each key in the map
    for key in Map_url_to_title_file_name:
        #initialize a list to store temporary vector
        temp_vector_list = []
        #loop through each index in the unique words list
        for idx in range(len(unique_words)):
            # Get the word from unique_words list
            word = unique_words[idx]
            
            # Get the tf-idf value of the word
            tf_idf_value = searchdata.get_tf_idf(key, word)
            
            # Append the tf-idf value to the temporary vector list
            temp_vector_list.append(tf_idf_value)
            
        #append the key to the temporary vector list
        temp_vector_list.append(key)
        #append the temporary vector list to the docs vector list
        docs_vector.append(temp_vector_list)
  
    #return the search words vector list
    return docs_vector


#🎆custom function
#function goal:
#calculate_cosine_similarity function calculates the cosine similarity between two vectors.
#inputs:
#function takes two inputs: 
#doc_vector: a list of numbers representing the tf-idf vector of one document.
#search_words_vector: a list of numbers representing the tf-idf vector of the search words.
#outputs:
#function returns a dictionary. the key is the url of the document and the value is the cosine 
#similarity between the document vector and the search words vector.
def calculate_cosine_similarity(doc_vector, search_words_vector):
    #initialize a dictionary to store cosine similarity
    cosine_similarity_dict = {}

    #pop the last element from the document vector and store it in url
    url = doc_vector.pop()
    #calculate the numerator of the cosine similarity
    numerator = sum(mult_elements_in_vectors(search_words_vector, doc_vector))
    #calculate the denominator of the cosine similarity
    denominator = math.sqrt(vector_square(doc_vector)*vector_square(search_words_vector))
    #if the denominator is not 0, calculate the cosine similarity
    if denominator != 0:
        cosine_similarity_dict[url] = numerator/denominator
    #if the denominator is 0, set the cosine similarity to 0
    else:
        cosine_similarity_dict[url] = 0
    
    #return the cosine similarity dictionary
    return cosine_similarity_dict


#🎆custom function
#function goal:
#sorted_dict function sorts a dictionary based on its values in descending order.
#inputs:
#function takes one input: 
#input_dict: a dictionary that needs to be sorted.
#outputs:
#function returns a dictionary sorted by its values in descending order. the keys 
#in the returned dictionary are the same as the input dictionary, but their order is 
#arranged according to their corresponding values in the input dictionary.
def sorted_dict(input_dict):
    #convert the dictionary to a list of tuples (key, value)
    items_list = []
    for key in input_dict:
        value = input_dict[key]
        pair = (key, value)
        items_list.append(pair)

    #sort the list of tuples based on the second element (value) using bubble sort
    for i in range(len(items_list)):
        for j in range(0, len(items_list)-i-1):
            # Compare items for sorting in descending order
            current_item = items_list[j]
            next_item = items_list[j+1]
            
            if current_item[1] < next_item[1]:
                # Swap items if current item is less than the next item
                temp = items_list[j]
                items_list[j] = items_list[j+1]
                items_list[j+1] = temp

    #convert the sorted list of tuples back to a dictionary
    sorted_dict = {}
    for item in items_list:
        sorted_dict[item[0]] = item[1]

    #return the sorted dictionary
    return sorted_dict



#function to search
def search(phrase, boost):
    #initialize a list to store results
    result_list = []
    #initialize a dictionary to store ranked pages
    ranked_page = {}
    #initialize a dictionary to store values for rank
    values_for_rank = {}
    
    #access the global variable
    global Map_url_to_title_file_name

    #check if the map of url to title file name is loaded
    if not is_Map_url_to_title_file_name_loaded:
        #if not, load the map from the json file
        with open("Map_url_to_title_file_name.json","r") as filein:
            Map_url_to_title_file_name = json.load(filein)  
    
    #loop through each vector in the document vector
    for vector in get_docs_vector(phrase):
        #update the values for rank dictionary with the cosine similarity
        values_for_rank.update(calculate_cosine_similarity(vector, get_search_words_vector(phrase)))    
    #if boost is not true
    if not boost:
        #sort the values for rank dictionary
        ranked_page = sorted_dict(values_for_rank)
        #initialize a counter
        a = 0
        #loop through each key in the ranked page
        for key in ranked_page:
            #initialize a dictionary to store result
            result_dict = {}
            #store the url, title and score in the result dictionary
            result_dict["url"] = key
            result_dict["title"] = Map_url_to_title_file_name[key][0]
            result_dict["score"] = ranked_page[key]
            #append the result dictionary to the result list
            result_list.append(result_dict)
            #increment the counter
            a += 1
            #if the counter reaches 10, break the loop
            if a == 10:
                break
        #return the result list
        return(result_list)
    #if boost is true
    else:
        #initialize a dictionary to store values for rank
        valuess_for_rank = {}
        #loop through each key in the values for rank dictionary
        for key in values_for_rank:
            #get the page rank
            page_rank = searchdata.get_page_rank(key)
            #calculate the values for rank
            valuess_for_rank[key] = values_for_rank[key]*page_rank
        #sort the values for rank dictionary
        ranked_page = sorted_dict(valuess_for_rank)
        #initialize a counter
        a = 0
        #loop through each key in the ranked page
        for key in ranked_page:
            #initialize a dictionary to store result
            result_dict = {}
            #store the url, title and score in the result dictionary
            result_dict["url"] = key
            result_dict["title"] = Map_url_to_title_file_name[key][0]
            result_dict["score"] = ranked_page[key]
            #append the result dictionary to the result list
            result_list.append(result_dict)
            #increment the counter
            a += 1
            #if the counter reaches 10, break the loop
            if a == 10:
                break
        #return the result list
        return(result_list)
    


#--------------------------------------------------------------------
#Commandline part
def read_search_config_from_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    phrase = lines[0].strip()
    boost = lines[1].strip().lower()
    file.close()
    return phrase + " " + boost

if __name__ == "__main__":
    config = read_search_config_from_file('search_config.txt')
    split_config = config.split()
    phrase = split_config[0]
    boost_str = split_config[1]
    if boost_str == 'true':
        boost = True
    else:
        boost = False
    results = search(phrase, boost)

    # Write the results to a JSON file
    with open('search_results.json', 'w') as filein:
        json.dump(results, filein)