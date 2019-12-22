# Low Level Text Search Engine
This is a low level text search engine using pure python and PyQt5 for an assignment in CPE651 (1/2019) class.

### Dataset
The testing data set is from http://web.eecs.umich.edu/~lahiri/gutenberg_dataset.html.

### How to use
1. Clone the repository.
2. Install required python3 libraries by running:
```
pip3 install -r lowLevelTextSearchEngine/requirements.txt
```
3. Download the data set and extract them.
4. Create "index" and "intermediate_index" folder inside that directory.
5. Run `python3 generate_index_dir.py` to generate necessary indices.
6. Once an index directory is created, you can either use a simple search script or one with GUI.
* If you want to use a script without GUI, run this following command:
```
python3 search_index_dir.py <query_str>
```
* Otherwise, you prefer to use a script with GUI, run this following command instead:
```
python3 simple_text_search_engine.py
```
