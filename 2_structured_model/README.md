# Structured (Non Linear) Models

To load the directory into the docker image:
`
docker run -v %cd%:/e -w /e --entrypoint bash --rm -it yijun/fast:ggnn
`

## Tree-based CNN (TBCNN)

The implementation is from [https://github.com/bdqnghi/bi-tbcnn].

Replace the `parser/run` file to our version. Then put the catagorized files into the srcs folder and run:

`
parser/run # has to be done in the docker image
`
`
python2 ast2vec/ast2vec/fast_merge_pickles_to_pickle.py ast2/left vec/left.pkl # has to be done in the docker image
`
`
python2 ast2vec/ast2vec/fast_merge_pickles_to_pickle.py ast2/right vec/right.pkl # has to be done in the docker image
`
`
python ast2vec/ast2vec/fast_pickle_file_to_training_trees.py vec/left.pkl vec/left_trees.pkl # has to be done in the docker image
`
`
python ast2vec/ast2vec/fast_pickle_file_to_training_trees.py vec/right.pkl vec/right_trees.pkl # has to be done in the docker image
`
`
python bi-tbcnn/bi-tbcnn/prepare_pairs_data.py vec/left_trees.pkl vec/right_trees.pkl model/all_training_pairs.pkl
`
`
python bi-tbcnn/bi-tbcnn/train_bitbcnn.py model/logs/training_log model/all_training_pairs.pkl vec/fast_pretrained_vectors_java.pkl vec/fast_pretrained_vectors_java.pkl
`
`
python bi-tbcnn/bi-tbcnn/test_bitbcnn.py model/logs/training_log model/all_training_pairs.pkl vec/fast_pretrained_vectors_java.pkl vec/fast_pretrained_vectors_java.pkl
`

## GGNN

We used the existing implementation from [https://github.com/bdqnghi/ggnn_graph_classification].

First log into the yijun/fast:ggnn docker image and then run:

`
fast -S -G src h.fbs
ggnn h.fbs train.txt test.txt
`

where src is the folder containing the Java source files. Serve the train/text txt files in the same format of programming_data/github_java_sort_function_babi folder. Then run:

`
python main_ggnn.py --cuda --training --directory program_data/atce --training_percentage 0.8 --n_classes 2
`
`
python main_ggnn.py --cuda --testing --directory program_data/atce --n_classes 2
`

for training and testing.