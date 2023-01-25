import mlconjug3
from mlconjug3.feature_extractor import extract_verb_features
from functools import partial

from hydra import compose, initialize
from omegaconf import OmegaConf


# context initialization
with initialize(version_base=None, config_path="config.yaml", job_name="train_model"):
    params = compose(config_name="config")
    print(OmegaConf.to_yaml(params))

# global initialization
initialize(version_base=None, config_path="config.yaml", job_name="train_model")
params = compose(config_name="config")
print(OmegaConf.to_yaml(params))


lang = params["language"]
output_folder = params["output_folder"]
split_proportion = params["split_proportion"]
dataset = mlconjug3.DataSet(mlconjug3.Verbiste(lang).verbs, vectorizer=params["vectorizer"])
model = mlconjug3.Model(language=lang, feature_selector=params["feature_selector"], classifier=params["classifier"])

ct = mlconjug3.utils.ConjugatorTrainer(lang=lang, output_folder=output_folder, split_proportion=split_proportion, dataset=dataset, model=model)

print("training model...")
ct.train()
print("model has benn trained.")

ct.predict()

print("evaluating model")
ct.evaluate()

print("saving model")
ct.save()
