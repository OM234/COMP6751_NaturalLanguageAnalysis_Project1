import nltk
from nltk.corpus import reuters
from Pipeline import Pipeline


def downloadReuters():
    nltk.download('reuters')


def main():
    downloadReuters()
    corpus = reuters

    # reuters corpus fileIDs to preprocess
    fileIDs = ['training/267', 'test/16213', 'teFst/18066', 'training/4425', 'test/14826', 'test/15910']
    for fileID in fileIDs:
        pipeline = Pipeline(corpus, fileID)  # create pipeline
        pipeline.preprocess()  # preprocess text
        pipeline.print_tokens()  # print values from pipeline
        pipeline.print_sentences()
        pipeline.print_pos_tags()
        pipeline.print_dates()
        pipeline.print_written_numbers()


if __name__ == "__main__":
    main()
