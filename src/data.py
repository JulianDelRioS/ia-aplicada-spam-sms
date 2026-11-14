"""Carga, validación, deduplicación y partición reproducible del SMS Spam Collection."""
import hashlib
import pathlib

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_raw() -> pd.DataFrame:
    path = ROOT / CFG["data"]["raw_path"]
    df = pd.read_csv(path, sep="\t", header=None, names=["label", "text"],
                     quoting=3, encoding="utf-8")
    print(f"Archivo: {path.name}  SHA-256: {sha256(path)}")
    return df


def validate(df: pd.DataFrame) -> None:
    print(f"Filas: {len(df)}  (esperado: 5574)")
    print("Distribución de clases:\n", df["label"].value_counts())
    assert set(df["label"]) == {"ham", "spam"}, "Etiquetas inesperadas"
    assert df["text"].notna().all(), "Hay textos vacíos"


def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    n_dup = df.duplicated(subset="text").sum()
    print(f"Mensajes duplicados (texto idéntico): {n_dup}")
    return df.drop_duplicates(subset="text").reset_index(drop=True)


def make_split(df: pd.DataFrame, seed: int) -> dict:
    d = CFG["data"]
    idx = df.index.to_series()
    train_idx, rest_idx = train_test_split(
        idx, test_size=d["val"] + d["test"], stratify=df["label"], random_state=seed)
    val_idx, test_idx = train_test_split(
        rest_idx, test_size=d["test"] / (d["val"] + d["test"]),
        stratify=df.loc[rest_idx, "label"], random_state=seed)
    return {"train": train_idx, "val": val_idx, "test": test_idx}


def main() -> None:
    df = load_raw()
    validate(df)
    df = deduplicate(df)
    out = ROOT / CFG["data"]["splits_dir"]
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "dataset_dedup.csv", index_label="id")
    splits = make_split(df, CFG["seed"])
    for name, ids in splits.items():
        ids.sort_values().to_csv(out / f"{name}_ids.csv", index=False, header=["id"])
        sub = df.loc[ids]
        print(f"{name}: {len(sub)} mensajes, {(sub.label == 'spam').mean():.1%} spam")
    # Control de fuga: ningún texto repetido entre particiones
    texts = {k: set(df.loc[v, "text"]) for k, v in splits.items()}
    assert not (texts["train"] & texts["test"]) and not (texts["val"] & texts["test"])
    print("Split congelado guardado en", out)


if __name__ == "__main__":
    main()
