import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd


class MethodLDA:
    def __init__(
        self, use_npy=False, topics=10, dataset="./all.txt", npy_dir="/data1/syx/"
    ):
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download("wordnet")
        self.methods = []
        self.ori_methods = []
        self.use_npy = use_npy
        self.topics = topics
        self.vectorizer = None
        self.lda = None
        self.dataset = dataset
        self.npy_dir = npy_dir

    def prepare_data(self):
        print("[prepare_data] preparing ...")
        data = []
        with open(self.dataset, "r") as fr:
            data = fr.readlines()
        self.ori_methods = data

        if self.use_npy:
            self.methods = self.load(os.path.join(self.npy_dir, "methods.txt"))
            print(f"[prepare_data] methods: {len(self.methods)}")
            return
        new_data = []
        amount = len(data)
        for cnt, d in enumerate(data):
            text = re.sub(r"[^a-zA-Z\s]", "", d)
            text = text.lower()
            words = word_tokenize(text)
            stop_words = set(stopwords.words("english"))
            words = [w for w in words if not w in stop_words]
            lemmatizer = WordNetLemmatizer()
            words = [lemmatizer.lemmatize(w) for w in words]
            new_data.append("".join(words))

            print(
                f"[prepare_data] {100*(cnt+1)/amount:.2f}%, {cnt+1}/{amount}", end="\r"
            )

        self.methods = new_data
        self.save(os.path.join(self.npy_dir, "methods.txt"), self.methods)
        print(f"[prepare_data] methods: {len(new_data)}")

    def save(self, path, _list):
        amout = len(_list)
        fname = os.path.basename(path)
        with open(path, "w") as f:
            for cnt, line in enumerate(_list):
                f.write(line + "\n")
                print(
                    f"[saving {fname}] {100*(cnt+1)/amout:.2f}%, {cnt+1}/{amout}",
                    end="\r",
                )

    def load(self, path):
        with open(path, "r") as f:
            return f.readlines()

    def convert2numercial(self):
        # if self.use_npy:
        #     self.methods = self.load(
        #         os.path.join(self.npy_dir, "methods(numercial).npy")
        #     )
        #     return
        print(f"[convert2numercial] converting ...")
        self.vectorizer = TfidfVectorizer()
        self.methods = self.vectorizer.fit_transform(self.methods)
        # self.save(os.path.join(self.npy_dir, "methods(numercial).npy"), self.methods)
        print(f"[convert2numercial] converted")

    def applay_lda(self):
        # if self.use_npy:
        #     self.lda = np.load(os.path.join(self.npy_dir, "lda.npy"))
        #     return
        print(f"[applay_lda] applaying ...")
        self.lda = LatentDirichletAllocation(n_components=self.topics, random_state=42)
        self.lda.fit(self.methods)
        # self.save(os.path.join(self.npy_dir, "lda.npy"), self.lda)
        print(f"[applay_lda] applayed")

    def assign_topic(self):
        print(f"[assign_topic] assigning ...")
        topic_assign = self.lda.transform(self.methods)
        topic_assign = np.argmax(topic_assign, axis=1)
        assigned = {"topic": [], "method": []}
        for m, topic in zip(self.ori_methods, topic_assign):
            assigned["topic"].append(topic)
            assigned["method"].append(m)
        df = pd.DataFrame(assigned)
        df.to_csv("./topic_assign.csv", index=False)
        print(f"[assign_topic] assigned")

    def run(self):
        self.prepare_data()
        self.convert2numercial()
        self.applay_lda()
        self.assign_topic()


if __name__ == "__main__":
    mLDA = MethodLDA()
    mLDA.run()
