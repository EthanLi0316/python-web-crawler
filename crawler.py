#import necessary libraries
import webdev
import json
import math


#🎆custom function
#function goal:
#extract_between_markers function extracts content between certain markers and stores them in a list.
#inputs:
#function takes three inputs: 
#s: a string from which content is to be extracted.
#start_marker: a string representing the start marker.
#end_marker: a string representing the end marker.
#outputs:
#function returns a list of strings. each string in the list is a content extracted from 
#the input string s that lies between the start_marker and the end_marker.
def extract_between_markers(s, start_marker, end_marker):
    #initialize variables
    i = 0
    contents = []
    #loop through the string
    while i < len(s):
        #find the start marker
        start_idex = s.find(start_marker, i)
        #break if start marker not found
        if start_idex == -1:
            break
        #find the end marker
        end_idex = s.find(end_marker, start_idex + len(start_marker) + 1)
        #break if end marker not found
        if end_idex == -1:
            break
        #extract the content between the markers
        content = s[start_idex + len(start_marker):end_idex]
        #append the content to the list
        contents.append(content)  
        #update the index
        i = end_idex + len(end_marker)
    #return the list of contents
    return contents


#🎆custom function
#function goal:
#get_absolute_url function constructs an absolute url from a relative url.
#inputs:
#function takes two inputs: 
#current_url: a string representing the current page's url.
#relative_url_in_current_page: a string representing a relative url found in the current page.
#outputs:
#function returns a string representing the absolute url. if the relative url 
# already starts with "http://", it returns the relative url as is. otherwise, 
# it constructs the absolute url by appending the relative url to the root of the current url.
def get_absolute_url(current_url, relative_url_in_current_page):
    #if the url already starts with "http://", return it as is
    if relative_url_in_current_page.startswith("http://"):
        return relative_url_in_current_page
    #otherwise, construct the absolute url
    relative_address = relative_url_in_current_page[1:]
    #loop through the current url in reverse
    for i in range(len(current_url)-1, -1, -1):
        #find the root of the current url
        if current_url[i] == "/":
            root = current_url[:i] 
            #return the absolute url
            return root + relative_address


#function to crawl a website starting from a seed url
def crawl(seed):
    #initialize variables
    word_document_count = {}  # Dictionary to count the number of documents each word appears in.
    total_documents = 0
    crawling_queue = [seed]
    crawled_urls = []
    file_name = -1
    Map_url_to_title_file_name = {}
    incoming_links = {}  
    outgoing_links = {}
    tf_values = {}  # Dictionary to store term frequencies. Key: (word, url), Value: tf value
    word_counts = {}  # Temporary dictionary to store word counts for each page. Key: url, Value: word count dict

    #start crawling
    while crawling_queue:
        #increment file name
        file_name += 1
        #get the current url
        current_url = crawling_queue.pop(0)
        #add the current url to the list of crawled urls
        crawled_urls.append(current_url)
        
        #read the content of the current url
        string = webdev.read_url(current_url)

        #extract titles, contents and relative urls from the current page
        titles = extract_between_markers(string, "<title>", "</title>")
        contents = extract_between_markers(string, "<p>", "</p>")
        relative_urls_in_current_page = extract_between_markers(string, 'href="' , '"')
        
        #initialize variables
        words_seen_in_current_document = {}
        word_count_for_current_document = {}  # Dictionary to count occurrences of each word in the current document
        total_words_in_current_document = 0
        
        #loop through the contents
        for content in contents:
            #split the content into words
            for words in content.split("\n"):
                for word in words.split():
                    #if the word is not empty
                    if word:
                        #increment the total words count
                        total_words_in_current_document += 1
                        #if the word is already in the dictionary, increment its count
                        if word in word_count_for_current_document:
                            word_count_for_current_document[word] += 1
                        #if the word is not in the dictionary, add it with a count of 1
                        else:
                            word_count_for_current_document[word] = 1
                        #add the word to the set of words seen in the current document
                        words_seen_in_current_document[word] = True

        #store word counts for the current page
        word_counts[current_url] = word_count_for_current_document

        #calculate term frequencies for the current document
        for word in word_count_for_current_document:
            count = word_count_for_current_document[word]
            tf = count / total_words_in_current_document
            key = str(current_url + " " + word)
            tf_values[key] = tf

        #update the word document count for each unique word seen in the current document
        for word in words_seen_in_current_document:
            if word not in word_document_count:
                word_document_count[word] = 1
            else:
                word_document_count[word] += 1

        #increment the total documents count
        total_documents += 1

        #loop through each relative url in the current page
        for relative_url_in_current_page in relative_urls_in_current_page:
            #get the absolute url
            absolute_url = get_absolute_url(current_url, relative_url_in_current_page)

            #if the absolute url is not already crawled or in the queue, add it to the queue
            if absolute_url not in crawled_urls and absolute_url not in crawling_queue:
                crawling_queue.append(absolute_url)

            #record the outgoing link
            if current_url not in outgoing_links:
                outgoing_links[current_url] = []
            if absolute_url not in outgoing_links[current_url]:
                outgoing_links[current_url].append(absolute_url)

            #record the incoming link
            if absolute_url not in incoming_links:
                incoming_links[absolute_url] = []
            if current_url not in incoming_links[absolute_url]:  # Check if the URL is already recorded
                incoming_links[absolute_url].append(current_url)

            #do file operations here for absolute_url

        #map the current url to its title and file name
        Map_url_to_title_file_name[current_url] = (titles[0], str(file_name) + ".txt")

    #calculate idf values
    idf_values = {}
    for word in word_document_count:
        doc_count = word_document_count[word]
        idf = math.log2(total_documents / (1 + doc_count))
        idf_values[word] = idf

    #dump idf values to a json file
    with open("idf_values.json", "w") as filein:
        json.dump(idf_values, filein)
    
    #dump tf values to a json file
    with open("tf_values.json", "w") as filein:
        json.dump(tf_values, filein)

    #dump map of url to title and file name to a json file
    with open("Map_url_to_title_file_name.json", "w") as filein:
        json.dump(Map_url_to_title_file_name, filein)

    #dump outgoing links to a json file
    with open("outgoing_links.json", "w") as filein:
        json.dump(outgoing_links, filein)
        
    #dump incoming links to a json file
    with open("incoming_links.json", "w") as filein:
        json.dump(incoming_links, filein)

    #return the total number of pages found
    return len(crawled_urls)


#--------------------------------------------------------------
#Commandline part
def read_seed_from_file(file_name):
    with open(file_name, 'r') as file:
        seed = file.read().strip()
    return seed

if __name__ == "__main__":
    seed = read_seed_from_file('crawler_config.txt')
    num_pages = crawl(seed)
    
    # Open the output file in write mode
    with open('crawler_output.txt', 'w') as file:
        # Write the number of pages to the file
        file.write(str(num_pages))