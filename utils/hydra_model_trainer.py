import mlconjug3
from mlconjug3.feature_extractor import extract_verb_features
from functools import partial
import hydra

@hydra.main(config_name="config")
def main(cfg):
    lang = cfg.language
    params = {'lang': lang,
              'output_folder': cfg.output_folder,
              'split_proportion': cfg.split_proportion,
              'dataset': mlconjug3.DataSet(mlconjug3.Verbiste(lang).verbs),
              'model': cfg.model
             }

    ct = mlconjug3.utils.ConjugatorTrainer(**params)

    print("training model...")
    ct.train()
    print("model has benn trained.")

    ct.predict()

    print("evaluating model")
    ct.evaluate()

    print("saving model")
    ct.save()

if __name__ == "__main__":
    main()

