import json
from pathlib import Path
from typing import List, Dict, Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from subprocess import run as run_subprocess, CalledProcessError


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def build_charts(artifacts_output_dir: Path) -> Dict[str, str]:
    charts_dir = ensure_dir(artifacts_output_dir / "charts")
    sns.set_theme(style="whitegrid")

    # Load data
    kpis_path = artifacts_output_dir / "kpis.json"
    mode_csv = artifacts_output_dir / "visites_par_mode.csv"
    secteur_csv = artifacts_output_dir / "visites_par_secteur.csv"

    kpis = load_json(kpis_path)

    # Monthly timeline from kpis
    monthly = kpis.get("visites_par_mois", [])
    months = [m.get("month") for m in monthly]
    counts = [m.get("count") for m in monthly]

    # Chart: Monthly visits (line)
    monthly_line = charts_dir / "visites_mensuelles_line.png"
    plt.figure(figsize=(12, 4))
    plt.plot(months, counts, marker="o", color="#4C78A8")
    plt.xticks(rotation=45, ha="right")
    plt.title("Visites par mois (timeline)")
    plt.ylabel("Visites")
    plt.tight_layout()
    plt.savefig(monthly_line, dpi=150)
    plt.close()

    import pandas as pd
    # Chart: Mode (bar)
    mode_bar = None
    if mode_csv.exists():
        df_mode = pd.read_csv(mode_csv)
        mode_bar = charts_dir / "visites_par_mode_bar.png"
        plt.figure(figsize=(6, 4))
        sns.barplot(data=df_mode, x="mode", y="visites", color="#F58518")
        plt.title("Répartition par mode de visite")
        plt.xlabel("")
        plt.ylabel("Visites")
        plt.tight_layout()
        plt.savefig(mode_bar, dpi=150)
        plt.close()

    # Chart: Secteur (bar)
    secteur_bar = None
    if secteur_csv.exists():
        df_secteur = pd.read_csv(secteur_csv)
        secteur_bar = charts_dir / "visites_par_secteur_bar.png"
        plt.figure(figsize=(7, 4))
        sns.barplot(data=df_secteur, x="secteur", y="visites", color="#54A24B")
        plt.title("Répartition par secteur")
        plt.xlabel("")
        plt.ylabel("Visites")
        plt.tight_layout()
        plt.savefig(secteur_bar, dpi=150)
        plt.close()

    # Extra charts from cleaned CSVs
    med_csv = artifacts_output_dir / "medecins_clean.csv"
    vis_csv = artifacts_output_dir / "visites_clean.csv"
    ars_bar = region_bar = spec_bar = delegue_bar = None
    if med_csv.exists():
        df_med = pd.read_csv(med_csv)
        if "ARS" in df_med.columns:
            tmp = df_med["ARS"].value_counts().reset_index()
            tmp.columns = ["ARS", "count"]
            ars_bar = charts_dir / "repartition_ars_bar.png"
            plt.figure(figsize=(7, 4))
            sns.barplot(data=tmp, x="ARS", y="count", color="#E45756")
            plt.title("Répartition par ARS (médecins)")
            plt.xlabel("")
            plt.ylabel("Médecins")
            plt.tight_layout(); plt.savefig(ars_bar, dpi=150); plt.close()
        if "Région" in df_med.columns:
            tmp = df_med["Région"].value_counts().reset_index()
            tmp.columns = ["Région", "count"]
            region_bar = charts_dir / "repartition_region_bar.png"
            plt.figure(figsize=(8, 4))
            sns.barplot(data=tmp, x="Région", y="count", color="#72B7B2")
            plt.title("Répartition par région (médecins)")
            plt.xlabel(""); plt.ylabel("Médecins")
            plt.xticks(rotation=30, ha="right")
            plt.tight_layout(); plt.savefig(region_bar, dpi=150); plt.close()
        # Specialités (1 et 2)
        spec_cols = [c for c in df_med.columns if c.startswith("Spécialité")]
        if spec_cols:
            tmp = pd.concat([df_med[c] for c in spec_cols], ignore_index=True)
            tmp = tmp.dropna()
            tmp = tmp.value_counts().head(10).reset_index()
            tmp.columns = ["Spécialité", "count"]
            spec_bar = charts_dir / "top10_specialites_bar.png"
            plt.figure(figsize=(8, 4))
            sns.barplot(data=tmp, x="count", y="Spécialité", color="#4C78A8")
            plt.title("Top 10 spécialités (médecins)")
            plt.xlabel("Médecins")
            plt.tight_layout(); plt.savefig(spec_bar, dpi=150); plt.close()
    if vis_csv.exists():
        df_vis = pd.read_csv(vis_csv)
        del_col = next((c for c in df_vis.columns if "delegue" in c.lower() or "délégué" in c.lower()), None)
        if del_col:
            tmp = df_vis[del_col].value_counts().head(10).reset_index()
            tmp.columns = ["Délégué", "visites"]
            delegue_bar = charts_dir / "top10_delegues_bar.png"
            plt.figure(figsize=(8, 4))
            sns.barplot(data=tmp, x="visites", y="Délégué", color="#F58518")
            plt.title("Top 10 délégués (visites)")
            plt.xlabel("Visites")
            plt.tight_layout(); plt.savefig(delegue_bar, dpi=150); plt.close()

    return {
        "monthly_line": str(monthly_line),
        "mode_bar": str(mode_bar) if mode_bar else None,
        "secteur_bar": str(secteur_bar) if secteur_bar else None,
        "ars_bar": str(ars_bar) if ars_bar else None,
        "region_bar": str(region_bar) if region_bar else None,
        "spec_bar": str(spec_bar) if spec_bar else None,
        "delegue_bar": str(delegue_bar) if delegue_bar else None,
    }


def build_manifest(artifacts_output_dir: Path, charts: Dict[str, str]) -> Path:
    kpis = load_json(artifacts_output_dir / "kpis.json")
    charts_abs = (artifacts_output_dir / "charts").absolute()
    
    bullets_objectifs = [
        "Objectif: construire un dashboard fiable et réplicable",
        "Lecture du cahier d'exercice et identification des onglets",
        "Sources: Données médecins + Données visites + Dashboard",
    ]

    bullets_methodo = [
        "Nettoyage: détection de l'entête (\"Identifiant\"), suppression lignes/colonnes vides",
        "Dates: conversion des numéros Excel en dates (origine: 1899-12-30)",
        "Durée: extraction en minutes depuis \"15 min\"",
        "Clés: \"Identifiant\" pour jointure entre visites et médecins",
    ]

    bullets_kpis = [
        f"Total de visites: {kpis.get('total_visites', '-')}",
        f"Médecins uniques visités: {kpis.get('unique_medecins_visites', '-')}",
        f"Durée moyenne de visite (min): {round(kpis.get('duree_moyenne_min', 0.0), 1) if kpis.get('duree_moyenne_min') else '-'}",
    ]

    bullets_formules = [
        "Totaux: =COUNTA('Données visites'![Identifiant])",
        "Uniques: =COUNTA(UNIQUE('Données visites'![Identifiant]))",
        "Répartition: =COUNTIF(col; étiquette) (Mode, Secteur, Délégué)",
        "Attributs médecins: XLOOKUP + SUMPRODUCT (ARS, Région, Spécialités)",
        "Justification: formules dynamiques, auditables, zéro valeurs codées en dur",
    ]

    bullets_qualite = [
        "Zéro erreur de formules (post-application + recalcul)",
        "Traçabilité: audit.json + artefacts (CSV, JSON, charts)",
        "Lisibilité: titres FR, légendes, unités explicites",
    ]

    bullets_justifs = [
        "Total visites: comptage des identifiants (toutes lignes non vides)",
        "Médecins uniques: UNIQUE sur \"Identifiant\"",
        "Mode/Secteur: COUNTIF sur colonnes correspondantes",
        "Délégué: COUNTIF sur \"Nom du délégué\"",
        "ARS/Région: SUMPRODUCT( XLOOKUP(Identifiant_visite → attribut_médecin) = libellé )",
        "Spécialités: SOMME des correspondances sur Spécialité 1 OU 2",
    ]

    slides: List[Dict[str, Any]] = [
        {"layout": "title", "title": "Test de dashboarding", "subtitle": "Synthèse, visuels et justifications"},
        {"layout": "bullets", "title": "Objectifs et données", "bullets": bullets_objectifs},
        {"layout": "bullets", "title": "Méthodologie de traitement", "bullets": bullets_methodo},
        {"layout": "bullets", "title": "Indicateurs clés", "bullets": bullets_kpis},
    ]

    if charts.get("monthly_line"):
        slides.append({
            "layout": "image",
            "title": "Série temporelle des visites",
            "image": charts["monthly_line"],
            "caption": "Visites par mois (2019–2021)"
        })
    if charts.get("mode_bar"):
        slides.append({
            "layout": "image",
            "title": "Répartition par mode",
            "image": charts["mode_bar"],
            "caption": "Face à face vs Interaction à distance"
        })
    if charts.get("secteur_bar"):
        slides.append({
            "layout": "image",
            "title": "Répartition par secteur",
            "image": charts["secteur_bar"],
            "caption": "S1..S6, S9"
        })
    if charts.get("ars_bar"):
        slides.append({
            "layout": "image",
            "title": "Répartition par ARS (médecins)",
            "image": charts["ars_bar"],
            "caption": "Comptage des médecins par ARS"
        })
    if charts.get("region_bar"):
        slides.append({
            "layout": "image",
            "title": "Répartition par région (médecins)",
            "image": charts["region_bar"],
            "caption": "Comptage des médecins par région"
        })
    if charts.get("spec_bar"):
        slides.append({
            "layout": "image",
            "title": "Top 10 spécialités (médecins)",
            "image": charts["spec_bar"],
            "caption": "Agrégation Specialité 1 + 2"
        })
    if charts.get("delegue_bar"):
        slides.append({
            "layout": "image",
            "title": "Top 10 délégués (visites)",
            "image": charts["delegue_bar"],
            "caption": "Comptage des visites par délégué"
        })

    slides.extend([
        {"layout": "bullets", "title": "Formules Excel et principes", "bullets": bullets_formules},
        {"layout": "bullets", "title": "Justification des réponses", "bullets": bullets_justifs},
        {"layout": "bullets", "title": "Qualité et validation", "bullets": bullets_qualite},
        {"layout": "title", "title": "Conclusion", "subtitle": "Dashboard fiable, reproductible et auditable"},
    ])

    manifest = {
        "title": "Test de dashboarding",
        "subtitle": "Synthèse, visuels et justifications",
        "assets_root": str(charts_abs),
        "slides": slides,
    }
    manifest_path = artifacts_output_dir / "presentation_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest_path


def build_pptx(artifacts_output_dir: Path, manifest_path: Path) -> Path:
    output_pptx = artifacts_output_dir / "dashboard_presentation_fr.pptx"
    cmd = [
        "python", "scripts/pptx/build_presentation.py", str(manifest_path), str(output_pptx)
    ]
    res = run_subprocess(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise CalledProcessError(res.returncode, cmd, res.stdout, res.stderr)
    return output_pptx


def main(artifacts_output_dir: str) -> None:
    out_dir = Path(artifacts_output_dir)
    charts = build_charts(out_dir)
    manifest = build_manifest(out_dir, charts)
    pptx_path = build_pptx(out_dir, manifest)
    print(json.dumps({
        "status": "success",
        "pptx": str(pptx_path),
        "charts": charts,
        "manifest": str(manifest),
    }, ensure_ascii=False))


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Build FR dashboard PPTX from artifacts")
    p.add_argument("artifacts_output_dir", type=str, help="Path to operation output dir with kpis.json & CSVs")
    args = p.parse_args()
    main(args.artifacts_output_dir)
