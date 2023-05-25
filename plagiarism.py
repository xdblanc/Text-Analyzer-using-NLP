import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx2txt

def plag(text):
    folder_name = "plag_files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    input_file_path = os.path.join(folder_name, "input.txt")
    with open(input_file_path, "w") as text_file:
        text_file.write(text)
    student_files = [os.path.join(folder_name, doc) for doc in os.listdir(folder_name) if doc.endswith(".txt")]
    file_content = [open(_file, encoding='utf8').read() for _file in student_files]

    def vectorize(text):
        return TfidfVectorizer().fit_transform(text).toarray()

    def similarity(doc1, doc2):
        return cosine_similarity([doc1], [doc2])[0][0]

    vectors = vectorize(file_content)
    s_vectors = list(zip(student_files, vectors))

    plagiarism_res = set()

    def checkplagiarism():
        for student_a, text_vector_a in s_vectors:
            new_vectors = s_vectors.copy()
            current_index = new_vectors.index((student_a, text_vector_a))
            del new_vectors[current_index]
            for student_b, text_vector_b in new_vectors:
                plagiarism_score = similarity(text_vector_a, text_vector_b)
                student_pair = sorted((student_a, student_b))
                score = (student_pair[0], student_pair[1], plagiarism_score)
                plagiarism_res.add(score)
        return plagiarism_res

    plagiarism_res_list = list(checkplagiarism())

    result_list = []

    for i in plagiarism_res_list:
        if input_file_path in i:
            result_list.append(i[2])

    return max(result_list)

x = plag("hi hello this is a sample file for plagiarism")
print(x)












# import os
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import docx2txt

# def plag(text):
#     text_file = open("input.txt", "w")
#     n = text_file.write(text)
#     text_file.close()
#     student_files = [doc for doc in os.listdir() if doc.endswith(".txt")]
#     file_content = [open(_file, encoding='utf8').read() for _file in student_files]

#     def vectorize(text):
#         return TfidfVectorizer().fit_transform(text).toarray()
#     def similarity(doc1, doc2):
#         return cosine_similarity([doc1], [doc2])[0][0]

#     vectors = vectorize(file_content)
#     s_vectors = list(zip(student_files,vectors))

#     plagiarism_res = set()

#     def checkplagiarism():
#         for student_a, text_vector_a in s_vectors:
#             new_vectors = s_vectors.copy()
#             current_index = new_vectors.index((student_a, text_vector_a))
#             del new_vectors[current_index]
#             for student_b, text_vector_b in new_vectors:
#                 plagiarism_score = similarity(text_vector_a, text_vector_b)
#                 student_pair = sorted((student_a, student_b))
#                 score = (student_pair[0], student_pair[1], plagiarism_score)
#                 plagiarism_res.add(score)
#         return plagiarism_res
    
#     plagiarism_res_list = list(checkplagiarism())

#     result_list = []
    
#     for i in plagiarism_res_list:
#         if('input.txt' in i):
#             result_list.append(i[2])
    
#     return max(result_list)

# x = plag("hi hello this is a sample file for plaigarism")
# print(x)

