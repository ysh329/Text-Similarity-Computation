# Text-Similarity-Computation
Text simlarity computation is very common, which is often used in repetition computation and relativity computation and etc.    
Current this project has finished text similarity compuation based on single word's cosine, which computes the similarity of two eassy's titles everytime.

## Cosine Similarity
Current(2015-8-31) I just finished the cosine similarity computation. Because of everytime we just need compute two (titles of essays)text, I made a tricky method to decrease the complexity of computation:    
1. Representing word vector(title of essay) in a sparse vector format;  
2. Computing the two text common existing words;  
3. In formula only computing not zero elements in word vector.  
