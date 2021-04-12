from flair.data import Corpus
from flair.datasets import UniversalDependenciesCorpus
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, FlairEmbeddings
from typing import List

# The hyper-parameters here are chosen according to the best-known
# configuration for FLAIR POS-tagging based on the PENN treebank
# reported here: https://github.com/flairNLP/flair/blob/master/resources/docs/EXPERIMENTS.md


# 1. get the corpus
corpus: Corpus = UniversalDependenciesCorpus(data_folder='AMALGUM_Flair')
# May need to change this depending on the relative location on your drive
# The data in AMALGUM_Flair are set up as follows:
# - all data are in .conll format, which is a standard for language tagging and will be recognized by FLAIR
# - the train and dev data sets are an equal split of all the (silver-tagged) AMALGUM data
# - the text data set is the whole of the (human-annotated) GUM Reddit data

# 2. what tag do we want to predict?
tag_type = 'pos'

# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

# initialize embeddings
embedding_types: List[TokenEmbeddings] = [
    WordEmbeddings('extvec'),
    FlairEmbeddings('news-forward'),
    FlairEmbeddings('news-backward'),
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# initialize sequence tagger
from flair.models import SequenceTagger

tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type)
# initialize trainer
from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)

trainer.train('resources/taggers/example-pos',
              train_with_dev=True,  
              max_epochs=150)

# Below is the setting Axel used to get this to run on a PC
# without CUDA enabled. This worked for about 14 days and then
# produced a "killed" message:
#trainer.train('resources/taggers/example-pos',
#              train_with_dev=True,  
#              max_epochs=15, # 150 is the suggested value in 
#              embeddings_storage_mode='none') # embeddings not stored in memory; is slow but keeps costs low. Other options: "cpu", "gpu2
