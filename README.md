# Egyptian Drug Database — قاعدة بيانات الأدوية المصرية

> **25,070 medicines registered in Egypt** with Arabic + English trade names, scientific composition, manufacturer, drug class, route of administration, and current EGP price.
>
> **25,070 دواء مسجل في مصر** مع الأسماء التجارية بالعربي والإنجليزي، التركيب العلمي، الشركة المنتجة، التصنيف الدوائي، طريقة الاستخدام، والسعر بالجنيه المصري.

![records](https://img.shields.io/badge/records-25%2C070-2ea44f)
![updated](https://img.shields.io/badge/updated-June%202026-blue)
![format](https://img.shields.io/badge/format-CSV%20%7C%20JSON-orange)
![license](https://img.shields.io/badge/license-CC0--1.0-lightgrey)

---

## What this is — ما هي هذه القاعدة

A clean, machine-readable dataset of medicines available in the Egyptian pharmaceutical market. Useful for pharmacy software, clinic management apps, prescription writing tools, drug-interaction services, medical search engines, RAG / LLM grounding, and academic research on pharmaceutical pricing.

قاعدة بيانات نظيفة وقابلة للقراءة آليًا للأدوية المتاحة في السوق المصري. مفيدة لتطبيقات الصيدليات، أنظمة العيادات، برامج كتابة الروشتات، خدمات التفاعلات الدوائية، محركات البحث الطبية، تطبيقات الذكاء الاصطناعي، والأبحاث الأكاديمية في مجال تسعير الأدوية.

**Last updated:** June 2026 — **آخر تحديث:** يونيو 2026

---

## Schema — البنية

| column | type | description (EN) | الوصف (AR) |
|---|---|---|---|
| `commercial_name_en` | string | English commercial / trade name | الاسم التجاري بالإنجليزية |
| `commercial_name_ar` | string | Arabic transliteration usable as a search alias | الاسم التجاري بالعربية (للبحث) |
| `scientific_name` | string | Active ingredient(s) / scientific composition | المادة الفعالة والتركيب العلمي |
| `manufacturer` | string | Manufacturer (`maker > parent group` if applicable) | الشركة المُصنِّعة |
| `drug_class` | string | Pharmacology / therapeutic class | التصنيف الدوائي |
| `route` | string | Route of administration (oral, topical, injection, ...) | طريقة الاستخدام |
| `price_egp` | number\|null | Current retail price in Egyptian pounds | السعر بالجنيه المصري |

---

## Sample — عيّنة

| commercial_name_en | commercial_name_ar | scientific_name | manufacturer | route | price_egp |
|---|---|---|---|---|---|
| PANADOL EXTRA 48 F.C. TABS. | بانادول إكسترا | CAFFEINE+PARACETAMOL | GLAXO SMITHKLINE | ORAL.SOLID | — |
| AUGMENTIN 1 GM 14 F.C. TABS. | أوجمنتين | AMOXICILLIN+CLAVULANIC ACID | GLAXO SMITHKLINE | ORAL.SOLID | — |
| BRUFEN 400 MG 30 TABS. | بروفين | IBUPROFEN | KAHIRA PHARM | ORAL.SOLID | — |
| ZITHROMAX 500 MG 3 F.C. TABS. | زيثروماكس | AZITHROMYCIN | PFIZER | ORAL.SOLID | — |
| CONGESTAL 20 TABS. | كونجيستال | CHLORPHENIRAMINE+PARACETAMOL+PSEUDOEPHEDRINE | KAHIRA PHARM | ORAL.SOLID | — |

---

## Files — الملفات

```
data/
├── egyptian-drugs.csv     # 3.6 MB, UTF-8, 25,070 rows
└── egyptian-drugs.json    # 7.6 MB, pretty-printed JSON array
```

Both files contain the **same records, same schema** — pick whichever fits your stack.

---

## Quick start — البدء السريع

### Python (pandas)

```python
import pandas as pd

drugs = pd.read_csv(
    "https://raw.githubusercontent.com/karem505/egyptian-drug-database/main/data/egyptian-drugs.csv"
)

# Search by Arabic name
drugs[drugs["commercial_name_ar"].str.contains("بانادول", na=False)]

# Cheapest paracetamol-containing drugs
mask = drugs["scientific_name"].str.contains("PARACETAMOL", na=False, case=False)
drugs[mask].nsmallest(10, "price_egp")
```

### Node.js

```javascript
const drugs = await fetch(
  "https://raw.githubusercontent.com/karem505/egyptian-drug-database/main/data/egyptian-drugs.json"
).then(r => r.json());

// Find every drug from a manufacturer
drugs.filter(d => d.manufacturer.includes("HIKMA"));
```

### SQL (DuckDB / SQLite)

```sql
-- DuckDB reads remote CSV directly
SELECT commercial_name_en, commercial_name_ar, price_egp
FROM 'https://raw.githubusercontent.com/karem505/egyptian-drug-database/main/data/egyptian-drugs.csv'
WHERE drug_class ILIKE '%antibiotic%'
ORDER BY price_egp DESC
LIMIT 50;
```

### curl

```bash
curl -sL https://raw.githubusercontent.com/karem505/egyptian-drug-database/main/data/egyptian-drugs.csv \
  | head
```

---

## Coverage — التغطية

| stat | value |
|---|---|
| Total records | **25,070** |
| Distinct trade-name brands | ~13,748 |
| Records with scientific composition | ~22,762 (≈ 91 %) |
| Records with drug class | ~24,973 (≈ 99.6 %) |
| Records with EGP price | 25,070 (100 %) |
| Records with Arabic alias | 25,070 (100 %) |
| Routes covered | oral solid, oral liquid, injection, topical, ophthalmic, vaginal, rectal, nasal, otic, inhalation, etc. |

---

## Notes on the Arabic column — ملاحظة عن العمود العربي

The `commercial_name_ar` field is a **deterministic phonetic transliteration** of the English trade name (e.g. `PANADOL → بانادول`, `AUGMENTIN → أوجمنتين`). It is intended as a **search alias** that matches what an Egyptian pharmacist or doctor would type when looking the drug up in Arabic — *not* the brand's officially registered Arabic mark, which is sometimes a different word entirely. For canonical Arabic naming, cross-reference the EDA (Egyptian Drug Authority) registry.

عمود `commercial_name_ar` يحتوي على **نقحرة صوتية حتمية** للاسم الإنجليزي (مثل `PANADOL ← بانادول`). الهدف منه أن يكون **اسمًا مرادفًا للبحث** يطابق ما يكتبه الصيدلي المصري عند البحث بالعربية، وليس بالضرورة الاسم العربي المسجل رسميًا.

---

## Use cases — حالات الاستخدام

- 🏥 **Clinic & pharmacy software** — drug autocomplete, prescription writing, point-of-sale
- 💊 **Drug-interaction checkers** — feed brand → active-ingredient resolution
- 🤖 **AI medical assistants** — RAG retrieval, LLM grounding for Egyptian-market drugs
- 📊 **Healthcare analytics** — pricing studies, market analysis, formulary planning
- 🎓 **Academic research** — pharmacoeconomics, public-health policy
- 🛒 **E-commerce** — pharmacy catalogs, comparison shopping
- 🔍 **Medical search engines** — Arabic + English unified lookup

أمثلة على الاستخدام: برامج العيادات والصيدليات، فاحص التفاعلات الدوائية، أدوات البحث الطبي بالذكاء الاصطناعي، التحليلات الصحية، الأبحاث الأكاديمية، تطبيقات التسوق للأدوية، محركات البحث الطبية ثنائية اللغة.

---

## Disclaimer — إخلاء مسؤولية

This dataset is provided **for informational and software-development purposes only**. Prices and availability change constantly; **always verify against the Egyptian Drug Authority (EDA / هيئة الدواء المصرية)** and a licensed pharmacist before clinical use. No warranty is given as to accuracy, completeness, or fitness for any medical purpose.

تُقدَّم هذه البيانات **لأغراض المعلومات وتطوير البرمجيات فقط**. الأسعار والمتاح يتغيران باستمرار؛ **يجب التحقق دائمًا مع هيئة الدواء المصرية وصيدلي مرخَّص** قبل أي استخدام إكلينيكي.

---

## License — الترخيص

Released under **Creative Commons Zero v1.0 Universal (CC0-1.0)** — public-domain dedication. You can copy, modify, and redistribute the data without permission or attribution. Full license text: <https://creativecommons.org/publicdomain/zero/1.0/>

البيانات متاحة تحت رخصة **المشاع الإبداعي صفر CC0-1.0** — ملكية عامة. يمكن النسخ والتعديل وإعادة التوزيع بدون إذن.

---

## Keywords — كلمات مفتاحية

Egyptian drug database · Egypt medicines list · Egyptian pharmacy data · drug prices Egypt · Arabic drug names · Egyptian medical dataset · pharmacy CSV · medicines JSON · EDA drugs · trade names Egypt · generic drugs Egypt · pharmaceutical database · clinic software dataset · prescription drugs Egypt · drug index Arabic English

قاعدة بيانات الأدوية المصرية · قائمة الأدوية في مصر · بنك الأدوية المصري · أسعار الأدوية المصرية · الأسماء التجارية للأدوية · أسماء الأدوية بالعربي · هيئة الدواء المصرية · أدوية الصيدليات · دليل الأدوية المصري · قاعدة بيانات الصيدلة · بيانات الأدوية مفتوحة المصدر · أسماء الأدوية الإنجليزية والعربية
