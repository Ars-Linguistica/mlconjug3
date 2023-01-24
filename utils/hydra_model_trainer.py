import mlconjug3
import hydra

@hydra.main(config_path="config.yaml")
def main(cfg):
    ct = ConjugatorTrainer(**cfg)

    ct.train()
    ct.predict()
    ct.evaluate()
    ct.save()
    

if __name__ == "__main__":
    main()

