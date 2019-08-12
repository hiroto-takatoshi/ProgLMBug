import javalang
import os
import codecs
import collections
import pickle
import fnmatch

PATH_TO_JAVA_PROJECTS="C:/Users/admin/repo_for_lm/java_projects"
PATH_TO_STORE_INDEXED_PROEJCTS ="C:/Users/admin/chenw2k/idx_pkl2/idx"
PATH_TO_STORE_THE_DICTIONARY="C:/Users/admin/chenw2k/dict_file_2"

vocabulary = []
vocabulary_size = 100000
max = 200000

def filter_token(token):
    numlist = [javalang.tokenizer.DecimalFloatingPoint, javalang.tokenizer.BinaryInteger, \
            javalang.tokenizer.DecimalInteger, javalang.tokenizer.FloatingPoint,\
            javalang.tokenizer.HexFloatingPoint, javalang.tokenizer.HexInteger,\
            javalang.tokenizer.Integer, javalang.tokenizer.OctalInteger]
    if type(token) in numlist: return "<num>", False
    elif type(token) == javalang.tokenizer.String: return "<str>", False
    else: return token.value, True


def tokenize(file):
    global vocabulary
    lines = file.read()
    try:
        tokens = javalang.tokenizer.tokenize(lines)
        for token in tokens:
            res, storeType = filter_token(token)
            vocabulary.append(res)
            if storeType: vocabulary.append(str(type(token)))
    except javalang.tokenizer.LexerError:
        print("Could not process " + file.name + "\n" + "Most likely are not Java")

def build_dict():
    global vocabulary
    global vocabulary_size
    count = [["<unk>", -1]]
    count.extend(collections.Counter(vocabulary).most_common(vocabulary_size-1))
    dictionary = {}
    for word, _ in count:
        dictionary[word] = len(dictionary)
    print(len(dictionary))
    unk_count = 0
    for word in vocabulary:
        index = dictionary.get(word, 0)
        if(index == 0):
            unk_count += 1
    count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return count,dictionary,reverse_dictionary

def file_to_ind(file,dictionary,index_path):
    lines = file.read()
    current_line = 1
    try:
        indexs = []
        tokens = javalang.tokenizer.tokenize(lines)
        for token in tokens:
            res = dictionary.get(filter_token(token)[0], 0)
            if res: 
                indexs.append(res)
            else:
                x = dictionary.get(str(type(token)), 0)
                assert x, str(type(token))
                indexs.append(x)

        with open(index_path, "wb") as f:
            pickle.dump(indexs, f)
    except javalang.tokenizer.LexerError:
        print("Could not process " + file.name + "\n" + "Most likely are not Java")

def main():
    global vocabulary
    global vocabulary_size
    global max

    dir_path = PATH_TO_JAVA_PROJECTS

    print("Building dictionary")

    count = 0
    for root, dirnames, filenames in os.walk(dir_path):
        for filename in fnmatch.filter(filenames, '*.java'):
            try:
                with codecs.open(os.path.join(root, filename), "r", encoding="UTF-8") as file:
                    tokenize(file)
                    count += 1
                if(count % 100 == 0):
                    print("Counting tokens, total: " + str(count) + " files")
                if(count >= max):
                    break
            except UnicodeDecodeError:
                try:
                    with codecs.open(os.path.join(root, filename), "r", encoding="ISO-8859-1") as file:
                        tokenize(file)
                        count += 1
                    if(count % 100 == 0):
                        print("Counting tokens, total: " + str(count) + " files")
                    if(count >= max):
                        break
                except UnicodeDecodeError:
                    print("Unkown encoding: " + os.path.join(root, filename))
                except:
                    pass
            except:
                pass

        if(count >= max):
            break

    print("Building dictionary")
    count,dictionary,reverse_dictionary = build_dict()

    print('Most common words (+UNK)', count[:10])

    count = 0
    index_path = PATH_TO_STORE_INDEXED_PROEJCTS
    for root, dirnames, filenames in os.walk(dir_path):
        for filename in fnmatch.filter(filenames, '*.java'):
            try:
                with codecs.open(os.path.join(root, filename), "r", encoding="UTF-8") as file:
                    file_to_ind(file, dictionary, index_path+str(count)+".pickle")
                    count += 1
                if(count % 100 == 0):
                    print("Indexed " + str(count) + " files")
                if(count >= max):
                    break
            except UnicodeDecodeError:
                try:
                    with codecs.open(os.path.join(root, filename), "r", encoding="ISO-8859-1") as file:
                        file_to_ind(file, dictionary, index_path+str(count)+".pickle")
                        count += 1
                    if(count % 100 == 0):
                        print("Indexed " + str(count) + " files")
                    if(count >= max):
                        break
                except UnicodeDecodeError:
                    print("Unkown encoding: " + os.path.join(root, filename))
                except:
                    pass
            except:
                pass

        if(count >= max):
                break

    for i in range(vocabulary_size):
        assert(reverse_dictionary[i])

    print("Saving count, dictionary, reverse_dictionary and vocabulary_size")

    with open(PATH_TO_STORE_THE_DICTIONARY , "wb") as f:
        pickle.dump([count,dictionary,reverse_dictionary,vocabulary_size],f)

    print("Done")

if __name__=="__main__":
    main()
