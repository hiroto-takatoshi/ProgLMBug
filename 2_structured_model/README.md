# Structured (Non Linear) Models

## Tree-based CNN (TBCNN)

The implementation is from [https://github.com/bdqnghi/bi-tbcnn].

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
python main_ggnn.py --cuda --testing --directory program_data/atce --n_classes 2
`

for training and testing.