### Python Web Crawler

- **Technologies**: Python
- **Description**: Developed a Python-based web crawler with a focus on minimizing runtime complexity. Utilized `os` and `json` modules for efficient data handling and reduced I/O operations. This project was created by Ethan Li and Bowen Zhang.

#### Instructions for Running the Crawler and Search Engine

##### Running the Crawler

1. **Open the Terminal**:
   - Ensure your command line is in the directory containing the project's Python files.

2. **Prepare the Configuration**:
   - Create a file named `crawler_config.txt` in the same directory. This file should contain the seed URL for the crawler without quotation marks.
   - Example seed URL: `http://people.scs.carleton.ca/~davidmckenney/fruits2/N-0.html`

3. **Execute the Crawler**:
   - In the terminal, type `python crawler.py` and press Enter.
   - The crawler will start processing the seed URL, and the output will be saved in `crawler_output.txt`.

##### Running the Search Engine

1. **Prepare the Configuration**:
   - Ensure you have a file named `search_config.txt` in the directory. This file should contain:
     - The search phrase on the first line.
     - The boost value (`True` or `False`) on the second line.
   - Example configuration:
     ```
     apple tomato tomato tomato
     True
     ```

2. **Execute the Search**:
   - In the terminal, ensure you are in the directory with `search.py` and `searchdata.py`.
   - Type `python search.py` and press Enter.
   - The search results will be stored in `search_results.json` in the same directory.
