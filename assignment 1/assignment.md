**How to build and run**

Run **test.ipynb** with Jupyter Notebook at root directory here we invoked all 5 classes which the assignmnets needed.

**Solution**

Input text (as raw string) is first shingled with k=9, then we tried to print the jaccard similarity between these shingled sets. For larger dataset, we generated 200 hash functions and used minhash to calculate its minhash signature, and finally, we used LSH with band size of 40 to find similar text pairs.

**Dataset**:  https://archive.ics.uci.edu/dataset/320/student+performance
We used one of the dataset student+performance is called : student-mat.csv, and we were only interested in 'Mjob' as the test data. 

