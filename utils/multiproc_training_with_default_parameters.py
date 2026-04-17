import mlconjug3
import numpy as np
from time import time
from joblib import Parallel, delayed
import joblib
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path

from sklearn.metrics import accuracy_score

np.random.seed(42)

langs = ("ro", "it", "en", "es", "fr", "pt")

OUTPUT_DIR = Path("trained_models")
OUTPUT_DIR.mkdir(exist_ok=True)

# --------------------------
# DATASETS
# --------------------------
print("\n[1/5] Building datasets...")

datasets = {
    lang: mlconjug3.DataSet(mlconjug3.Verbiste(language=lang).verbs)
    for lang in langs
}

for lang, ds in datasets.items():
    ds.split_data(proportion=0.8)  # ✅ USE BUILT-IN SPLIT
    print(
        f"  ? {lang}: "
        f"total={len(ds.verbs_list)} | "
        f"train={len(ds.train_input)} | "
        f"test={len(ds.test_input)}"
    )

print("\n[2/5] Training models in parallel...\n")


# --------------------------
# MODEL FACTORY
# --------------------------
def build_model(lang: str):
    return mlconjug3.Model(language=lang)


# --------------------------
# TRAIN FUNCTION
# --------------------------
def train_one(lang: str):
    print(f"[TRAIN] {lang} starting...")
    start = time()

    model = build_model(lang)
    ds = datasets[lang]

    # ✅ TRAIN USING DATASET API
    model.train(ds.train_input, ds.train_labels)

    t = time() - start
    print(f"[TRAIN] {lang} done in {t:.2f}s")

    return lang, model, t


# --------------------------
# PARALLEL TRAINING
# --------------------------
results = Parallel(n_jobs=min(len(langs), 4))(
    delayed(train_one)(lang) for lang in langs
)

models = {}
training_times = {}

for lang, model, t in results:
    models[lang] = model
    training_times[lang] = t


# --------------------------
# EVALUATION (REAL)
# --------------------------
print("\n[3/5] Evaluating models...\n")

for lang in langs:
    ds = datasets[lang]

    pred = models[lang].predict(ds.test_input)
    true = ds.test_labels

    acc = accuracy_score(true, pred)
    print(f"{lang.upper():2}: acc={acc:.4f}")


# --------------------------
# SAVE MODELS
# --------------------------
print("\n[4/5] Saving models...\n")

for lang in langs:
    model_path = OUTPUT_DIR / f"trained_model-{lang}-final.pickle"
    zip_path = OUTPUT_DIR / f"trained_model_{lang}.zip"

    joblib.dump(models[lang], model_path)

    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        zf.write(model_path, arcname=model_path.name)

    model_path.unlink()

    print(f"  ? Saved {zip_path}")


# --------------------------
# FINAL REPORT
# --------------------------
print("\n[5/5] Final Training Report\n")

report = []

for lang in langs:
    ds = datasets[lang]

    pred = models[lang].predict(ds.test_input)
    true = ds.test_labels

    acc = float(np.mean(pred == true))
    misses = int(np.sum(pred != true))
    total = len(true)
    time_sec = training_times[lang]

    report.append((lang, acc, misses, total, time_sec))

report.sort(key=lambda x: x[1])

for lang, acc, misses, total, time_sec in report:
    print(
        f"{lang}: "
        f"acc={acc:.4f} | "
        f"miss={misses} | "
        f"n={total} | "
        f"time={time_sec:.2f}s"
    )

best = max(report, key=lambda x: x[1])[0]
worst = min(report, key=lambda x: x[1])[0]

print(f"\nBest: {best} | Worst: {worst}")
