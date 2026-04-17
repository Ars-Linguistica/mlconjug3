import mlconjug3
import numpy as np
from time import time
from joblib import Parallel, delayed
import joblib
from zipfile import ZipFile, ZIP_DEFLATED
from pathlib import Path
from collections import Counter, defaultdict

from sklearn.metrics import accuracy_score, confusion_matrix

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
    ds.split_data(proportion=0.8)
    print(
        f"  ? {lang}: total={len(ds.verbs_list)} | "
        f"train={len(ds.train_input)} | test={len(ds.test_input)}"
    )

print("\n[2/5] Training models in parallel...\n")


def build_model(lang: str):
    return mlconjug3.Model(language=lang)


def train_one(lang: str):
    print(f"[TRAIN] {lang} starting...")
    start = time()

    model = build_model(lang)
    ds = datasets[lang]

    model.train(ds.train_input, ds.train_labels)

    t = time() - start
    print(f"[TRAIN] {lang} done in {t:.2f}s")

    return lang, model, t


results = Parallel(n_jobs=min(len(langs), 4))(
    delayed(train_one)(lang) for lang in langs
)

models = {}
training_times = {}

for lang, model, t in results:
    models[lang] = model
    training_times[lang] = t

# --------------------------
# EVALUATION
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
# ERROR ANALYSIS (RO + IT)
# --------------------------
print("\n[6/6] ERROR ANALYSIS (RO + IT)\n")


def error_analysis(lang):
    print("\n==============================")
    print(f" ERROR ANALYSIS: {lang.upper()}")
    print("==============================\n")

    ds = datasets[lang]
    model = models[lang]

    y_true = ds.test_labels
    y_pred = model.predict(ds.test_input)

    acc = accuracy_score(y_true, y_pred)
    print(f"Accuracy: {acc:.4f}\n")

    # confusion pairs
    conf = Counter()
    for t, p in zip(y_true, y_pred):
        if t != p:
            conf[(t, p)] += 1

    print("Top confusion pairs:\n")
    for (t, p), c in conf.most_common(15):
        print(f"{t} ? {p} : {c}")

    # examples
    print("\nSample misclassified verbs:\n")

    grouped = defaultdict(list)
    for verb, t, p in zip(ds.test_input, y_true, y_pred):
        if t != p:
            grouped[(t, p)].append(verb)

    for (t, p), verbs in list(grouped.items())[:5]:
        print(f"\n{t} ? {p} ({len(verbs)} cases)")
        print("Examples:", verbs[:10])


error_analysis("ro")
error_analysis("it")

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
