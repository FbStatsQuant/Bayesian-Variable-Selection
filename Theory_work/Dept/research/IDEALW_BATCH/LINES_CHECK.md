# LINES_CHECK — IDEAL-W⁺ batch NARROW (19 claims) + errata

Run 2026-11-16 05:59 CST against origin/main 967313dd (registry `claims.tsv` and every target file as on origin/main). Method: the origin/main files and copies patched by `patches/*.patch` (scratch outside the repo, since deleted); `git apply --check` passes for all 20 patches on an origin/main tree, and the applied result is byte-identical to the generator's output. Hashes follow the registry rule: span hash = `bvsreg.text_hash` (lines rstripped, LF-joined, sha256); claim hash = `bvsreg.claim_hash` (statement span, then each premise span after its `--premise path--` marker). Recomputed before the patch, the claim hash equals the stored `sha256` for all 99 rows checked (0 mismatches), which validates the method.

**Result: PASS — no registered or cited span moves.** Every in-place edit replaces a line by one line (same line count inside every span); every narrowing note / erratum is appended after the old last line. Hash changes: exactly the 19 batch rows that carry an every-n/asymptotic delivery sentence in their span or premises (16 by statement span, X10 by premise `STATEMENT_T2.md:61-62`), **plus W1C-FINAL:Lemma-CAP** (premise `s7_impl.tex:36-43` contains the :39 erratum; its statement span 45-56 is unchanged). Two batch rows keep their hash: **W2-FAC-B:L5** (span 44-45 is the (C3) consistency theorem; its delivery text L5.4 lies outside any span, edited in place at :61) and **W2-FAC-S5:L5** (span 33-37 is (C3-R); its delivery part is the separate row W2-FAC-S5:L5.C4-R, narrowed). For those two the recorder edits only `short`/`notes` (they mention delivery).

## 0. Files and lines
| file | lines | changed lines (old numbering) | sha256 before → after (LF-normalised whole file) |
|---|---|---|---|
| `Wave1C/C-DLV/INVENTORY.md` | 81 → 93 | 80 (Summary; no registered span in this file); section X′ appended 82-93 — ERRATUM | `de7188d81864c42b…` → `220efcad1a7fb82e…` |
| `Wave1C/C-DLV/lemmas/L2_degenerate.md` | 70 → 72 | none; erratum appended 71-72 (span 37-67 untouched) — ERRATUM | `6d46b556a6c8adb5…` → `fff0ae3f003365a4…` |
| `Wave1C/C-DLV/STATEMENT.md` | 84 → 86 | none; amendment note appended 85-86 (C-DLV:O / Prop-F spans end at 84, unchanged) — ERRATUM | `464d659ac3807579…` → `517f0f91dc386661…` |
| `Wave1C/FINAL/sections/s7_impl.tex` | 82 → 82 | 39 (inside premise span 36-43 of W1C-FINAL:Lemma-CAP) — ERRATUM | `eff77ee7400df48b…` → `5de4913f483695fa…` |
| `Wave1C/HQ_AUDIT/A2_propF_GROW.md` | 67 → 71 | 27 (in span 5-35); note appended 68-71 | `ab143d1b8b201f66…` → `b203ab2540d52f21…` |
| `Wave1C/HQ_AUDIT/A3_check_A2.md` | 43 → 47 | 5 (= span 5-5); note appended 44-47 | `b652f0e8942b3e39…` → `6cedc4db34d457b3…` |
| `Wave2/W2-FAC-A/lemmas/L7_delivery.md` | 53 → 57 | 22, 23 (in span 22-24); note appended 54-57 | `7b1a936445bf6828…` → `1141586a3573a442…` |
| `Wave2/W2-FAC-A/STATEMENT.md` | 185 → 189 | 133 (in span 102-152); note appended 186-189 | `d04413f0445a6a5a…` → `3626330e9ec18f69…` |
| `Wave2/W2-FAC-B/lemmas/L5_assembly.md` | 68 → 68 | 61 (outside every registered span; L5.4 step (2)); no append | `d8a5a6f9890754bd…` → `a2a170eb4585ba11…` |
| `Wave2/W2-FAC-B/STATEMENT.md` | 159 → 163 | 131 (in span 105-134); note appended 160-163 | `bf18b602424855b6…` → `93e1e945d0230b74…` |
| `Wave2/W2-FAC-PK/STATEMENT.md` | 121 → 125 | 82 (in span 73-87); note appended 122-125 | `192d65495ce4b2cf…` → `edd5108acc207f8a…` |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md` | 56 → 60 | 41 (in span 39-43 of L5.C4-R; outside L5's 33-37); note appended 57-60 | `6c70772d89d297be…` → `5648edebb2643eba…` |
| `Wave2/W2-FAC-S5/STATEMENT.md` | 148 → 152 | 124 (in span 112-124); note appended 149-152 | `99f13e49d3d2868e…` → `32d293e75ae25a3a…` |
| `Wave2/W2-FAC-XA/STATEMENT.md` | 110 → 114 | 86 (in span 85-86); note appended 111-114 | `e754526598d5190c…` → `0777647a02b2d10b…` |
| `Wave2/W2-FAC-X/lemmas/X10_assembly_T2.md` | 22 → 22 | 21 (outside X10's span 1-1; (G4) paragraph); no append | `24024393ab688add…` → `c500b350763890a4…` |
| `Wave2/W2-FAC-X/STATEMENT.md` | 126 → 130 | 94 (in span 76-95); note appended 127-130 | `f6e011fd028f082d…` → `dbf90d03df79cb39…` |
| `Wave2/W2-FAC-X/STATEMENT_T2.md` | 84 → 88 | 62 (in span 49-62 and in X10's premise 61-62); note appended 85-88 | `48078b426f8cf866…` → `3e7da6d058dd0bb0…` |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md` | 39 → 43 | 17 (in premise span 17-19 of F-LOC2.exp/.poly); note appended 40-43 | `d7720883d875c779…` → `aeab5c89306a175d…` |
| `Wave2/W2-LOC2/STATEMENT.md` | 118 → 122 | 101 (in span 100-102); note appended 119-122 | `aa074a55826a08b8…` → `b955f083e7721f6f…` |
| `Wave2/W2-UNI/STATEMENT.md` | 195 → 199 | 109 (in UNI-0 103-110), 123 (in UNI-1 112-131); note appended 196-199 | `925a9eb3646720c0…` → `8b96e79b2533937d…` |

Full whole-file hashes (for IMPACT / manifest re-freezes):
```
Theory_work/Wave1C/C-DLV/INVENTORY.md
  before de7188d81864c42b0a6cb18c803780d6cf06eea7ea43df0df9fd438fbc3395fe
  after  220efcad1a7fb82e1e8ce12d614b7d3b6d7d2401b9b1ca876d189c8ee120f913
Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md
  before 6d46b556a6c8adb5caca016c0ce4f3782eae0acd4148a0f451114ffbe8b583aa
  after  fff0ae3f003365a46f3ff8adbc8d210744f78b801db631a7bfdb54e7e9ac0630
Theory_work/Wave1C/C-DLV/STATEMENT.md
  before 464d659ac3807579dbe9ce6f3673f1416b98792f6bf162425abc7d3b0ee1cad5
  after  517f0f91dc386661fe1a74dbb5fe4650129d7ecaa180b13a78a9ca0e53757d43
Theory_work/Wave1C/FINAL/sections/s7_impl.tex
  before eff77ee7400df48b7a248d245af1158cdf4c89ff6de7e8efcbed6089fdd2f3d3
  after  5de4913f483695fa19e0af59934b77182639b5e0e29cf4fe2e324b52778be0fe
Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md
  before ab143d1b8b201f66ec000313b59ecacd1d2e95bce067512b6762aaf4e21c5e79
  after  b203ab2540d52f219b2c67bf19205b89a5b2242b52ee1ad9f2f4deb6c0978c83
Theory_work/Wave1C/HQ_AUDIT/A3_check_A2.md
  before b652f0e8942b3e39f0cb76916edcf2c5ed762a77cd2ffd3b846f201956bdf25b
  after  6cedc4db34d457b376f9bdeaa46403cfbfdd8e51698239eae0b85740f2f32dd2
Theory_work/Wave2/W2-FAC-A/lemmas/L7_delivery.md
  before 7b1a936445bf682892ccec87fa6f06301b75a72b9b89a8d3a00bd7dcb705d41a
  after  1141586a3573a4424268210995484a324a7eae7947a78dec4bf8fd46962b8891
Theory_work/Wave2/W2-FAC-A/STATEMENT.md
  before d04413f0445a6a5a0189315719572cb988dfa09dd24e61be53d4f9419440802e
  after  3626330e9ec18f6949ccfa2f9ae2658c8ffd7b60418a96ce09e30d404c78df7f
Theory_work/Wave2/W2-FAC-B/lemmas/L5_assembly.md
  before d8a5a6f9890754bde3a207d5c50eba0bcaf08815290513f8945319408bc48354
  after  a2a170eb4585ba110c22e058c6b438574481ca857f22613db21d959f291aca34
Theory_work/Wave2/W2-FAC-B/STATEMENT.md
  before bf18b602424855b6dded905077176790855127a25527916146d152ba4053610e
  after  93e1e945d0230b74e68a28e80bfaf6f3a7b2e6f77cc0074db33f7c298c4933b3
Theory_work/Wave2/W2-FAC-PK/STATEMENT.md
  before 192d65495ce4b2cf2d7b06254423f9d7a3216a5dff8ad13ca85ecdfcf59fca54
  after  edd5108acc207f8a6f925f9e508b5add71cb3681ff53d0bb588bc3f9f26a0968
Theory_work/Wave2/W2-FAC-S5/lemmas/L5_assembly.md
  before 6c70772d89d297be9eea1735fa25fd9a4eab66f749a1dcd29e26fb8532e82dd1
  after  5648edebb2643eba947211f7a756551b393b9495abbe5f15fce16ea721a9f15a
Theory_work/Wave2/W2-FAC-S5/STATEMENT.md
  before 99f13e49d3d2868e1a41fc96020661ed015196288b36f301246ca1697de2fe62
  after  32d293e75ae25a3a309faee9ac1d0d084664e2b665234b7b782b9477926c7a30
Theory_work/Wave2/W2-FAC-XA/STATEMENT.md
  before e754526598d5190c00b96bcb3a1f7127160d89b271e559193dc3fbfba31f3c7c
  after  0777647a02b2d10b3270f7c540052048a060d9613afcdf81f664740badafdb53
Theory_work/Wave2/W2-FAC-X/lemmas/X10_assembly_T2.md
  before 24024393ab688add32022912f45b276335db20b81a1535c90b2d66e77c2ac4db
  after  c500b350763890a4cbe1c3a986c09634c14eeb67f9ecdbae0672e7215805eadc
Theory_work/Wave2/W2-FAC-X/STATEMENT.md
  before f6e011fd028f082d027ea1f1ff9d5d6a9d22287b8394cb14a3a554436571f547
  after  dbf90d03df79cb39476633078829e76423f78e18d0c044301c58d119979d5fe4
Theory_work/Wave2/W2-FAC-X/STATEMENT_T2.md
  before 48078b426f8cf866f002b8525ff414d151792f5bbd1d83b6b334f0dad095174a
  after  3e7da6d058dd0bb07c7d58b093b0d61018528775c83841d3ba6468b8f7737ecd
Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md
  before d7720883d875c779b52563eba21d1879071ad63987602cde9203b8de68974eae
  after  aeab5c89306a175defcd98ef45f4f85fc307e39429bbae670b0469fc451d92d2
Theory_work/Wave2/W2-LOC2/STATEMENT.md
  before aa074a55826a08b8870c69248fa1a88688172c56917a474847daade06717525a
  after  b955f083e7721f6f96c6e5ad9f0cc6b16364d72e2180fef1503ab0327aa982df
Theory_work/Wave2/W2-UNI/STATEMENT.md
  before 925a9eb3646720c007c63912c7357a73461d01fe7495e8741e45d0b2f2042321
  after  8b96e79b2533937db28a87568b359e827350fa9cf0628ab89f120d66e8590b0b
```

## A. Every claims.tsv row whose file or a premise file is touched
Batch rows in **bold**. `claim_hash before` equals the stored `sha256` in every row.

| id | span | span changed? | claim_hash before (= stored) | claim_hash after | changed? | version → proposed |
|---|---|---|---|---|---|---|
| C-DLV:Target-T | Wave1C/C-DLV/STATEMENT.md:48-49 | no | `1d12fca353cb7b1d6442a61cd9b15b0d56625e8f5974e96660c9a0daec5a3ab9` | `1d12fca353cb7b1d6442a61cd9b15b0d56625e8f5974e96660c9a0daec5a3ab9` | no | 1.0.0 |
| C-DLV:P1-Inventory | Wave1C/C-DLV/STATEMENT.md:52-53 | no | `0d005230e694305e0b60ae5af9ec663e2927a08ee3b217dabd7f0416abd590dc` | `0d005230e694305e0b60ae5af9ec663e2927a08ee3b217dabd7f0416abd590dc` | no | 1.0.0 |
| C-DLV:L1-R | Wave1C/C-DLV/lemmas/L1_resources.md:70-81 | no | `7dde53124070330b1c44c95e9f571647b02c7f0dc1ac11fd534dbf786bc4745c` | `7dde53124070330b1c44c95e9f571647b02c7f0dc1ac11fd534dbf786bc4745c` | no | 1.0.0 |
| C-DLV:Cor-R | Wave1C/C-DLV/lemmas/L1_resources.md:129-143 | no | `91e520d80f84e21d04f5ac85641d19bbdcf729d2a313491ce9716fdd6a93cc4e` | `91e520d80f84e21d04f5ac85641d19bbdcf729d2a313491ce9716fdd6a93cc4e` | no | 1.0.0 |
| C-DLV:L2-S1 | Wave1C/C-DLV/lemmas/L2_degenerate.md:5-18 | no | `78615b44abdec3824c367b5c4288d542b477756996fac78bdec71212e19ec6ea` | `78615b44abdec3824c367b5c4288d542b477756996fac78bdec71212e19ec6ea` | no | 1.0.0 |
| C-DLV:L2-S2 | Wave1C/C-DLV/lemmas/L2_degenerate.md:20-35 | no | `b0a9ac4e8ec8b349a0256d63953eb72a2dcd20208a6606be77106beef7a0612a` | `b0a9ac4e8ec8b349a0256d63953eb72a2dcd20208a6606be77106beef7a0612a` | no | 1.0.0 |
| C-DLV:L2-S3 | Wave1C/C-DLV/lemmas/L2_degenerate.md:37-67 | no | `790f1b8980833e1c2f757628127ef5328d9859ccb67ebac1188eaf82d685c87f` | `790f1b8980833e1c2f757628127ef5328d9859ccb67ebac1188eaf82d685c87f` | no | 1.0.0 |
| C-DLV:Thm-D | Wave1C/C-DLV/lemmas/L4_delivery.md:13-22 | no | `16301ea60d71311604f51985004015c3842c608485d3437c8e8847b8a1969895` | `16301ea60d71311604f51985004015c3842c608485d3437c8e8847b8a1969895` | no | 1.0.0 |
| C-DLV:Cor-Dp | Wave1C/C-DLV/STATEMENT.md:75-76 | no | `7d6cc75f64d1687176bac2cb1543de982ea98c858345a49e4eed41e9c252f578` | `7d6cc75f64d1687176bac2cb1543de982ea98c858345a49e4eed41e9c252f578` | no | 1.0.0 |
| C-DLV:C1-CondDelivery | Wave1C/C-DLV/STATEMENT.md:68-74 | no | `240e0d525e6c8857b0747b0d580a4129e270fd3d39d3208cd13f38ed4d60555e` | `240e0d525e6c8857b0747b0d580a4129e270fd3d39d3208cd13f38ed4d60555e` | no | 1.0.0 |
| C-DLV:Prop-F | Wave1C/C-DLV/lemmas/L4_delivery.md:79-84 | no | `9cb1d6ee5cee91b6862d582cf39aed9053d84e993f8b471488f0f66833a2331d` | `9cb1d6ee5cee91b6862d582cf39aed9053d84e993f8b471488f0f66833a2331d` | no | 1.0.0 |
| C-DLV:O | Wave1C/C-DLV/STATEMENT.md:79-84 | no | `3f9b4aee0e69a36266a1d77599083767fb3c64d9d592acc2325c1e2b58ef20c5` | `3f9b4aee0e69a36266a1d77599083767fb3c64d9d592acc2325c1e2b58ef20c5` | no | 1.0.0 |
| W1C-FINAL:Lemma-CAP | Wave1C/FINAL/sections/s7_impl.tex:45-56 | no | `5141210f02a82a89dcfa14af48c2d7c0569fb523addddca7c98ddab92b1fe10a` | `fc6d4753df2ab75b7f5c0aabe7723814c6d57de9f533fe8357caf1d3e76d00ad` | **YES** | 1.0.0 → patch bump (premise erratum, no statement change) |
| **HQ_AUDIT-W1C:A2** | Wave1C/HQ_AUDIT/A2_propF_GROW.md:5-35 | YES | `c6235c906db73dcbf67962ee7571e45df2ba23ed3444d45ad5237259a9ca4dd5` | `4e45c8d0a63c916f921381a81a5a22823b0034f63e26542ea84f4d4e4f1f12f3` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| **HQ_AUDIT-W1C:A3** | Wave1C/HQ_AUDIT/A3_check_A2.md:5-5 | YES | `665ea7cd3df52a9045b00e029603cd0fbc892b3a4a03889389e4cf914049ea66` | `dcdc12e374084dfb322899184cfdb32531d6bad75adc106513e222c66766f7d8` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| **W2-FAC-A:Thm-FAC-L** | Wave2/W2-FAC-A/STATEMENT.md:102-152 | YES | `88e789bd4dc30d96f0c04cf6511b1e256162bbd5c8f57e3d14a15d0087d46c0d` | `e5d2037c69d8441d88077c79e477505611bbfeda6b97b75c81a1c88e4e33e5bc` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-A:Prop-SHARP | Wave2/W2-FAC-A/STATEMENT.md:154-159 | no | `eb35eedd4f9857324811be56c884325ab6d61e7c49de2b0473a0209142034858` | `eb35eedd4f9857324811be56c884325ab6d61e7c49de2b0473a0209142034858` | no | 1.0.0 |
| W2-FAC-A:L1 | Wave2/W2-FAC-A/lemmas/L1_uniform_add.md:149-154 | no | `806f5a32cde1d78f1dbbc3666767b510b9364ff7fe48531d59873c6ea1716f17` | `806f5a32cde1d78f1dbbc3666767b510b9364ff7fe48531d59873c6ea1716f17` | no | 1.0.1 |
| W2-FAC-A:L2 | Wave2/W2-FAC-A/lemmas/L2_sandwich.md:13-13 | no | `ceee6c064cb19081ab75c6d95045e90da27deea7bd345b7a1be6b03a6c5a8489` | `ceee6c064cb19081ab75c6d95045e90da27deea7bd345b7a1be6b03a6c5a8489` | no | 1.0.0 |
| W2-FAC-A:L3.1 | Wave2/W2-FAC-A/lemmas/L3_NA_TL.md:34-34 | no | `635c240e9ea25baf8ace2f13c1bee433836b0ef0d85864a5ef388893eeb6bdd1` | `635c240e9ea25baf8ace2f13c1bee433836b0ef0d85864a5ef388893eeb6bdd1` | no | 1.0.0 |
| W2-FAC-A:L3.2 | Wave2/W2-FAC-A/lemmas/L3_NA_TL.md:62-62 | no | `80611338e2dd432946d6483791fff8de5f4e8963c5f03b5d6b77b8f26eceb847` | `80611338e2dd432946d6483791fff8de5f4e8963c5f03b5d6b77b8f26eceb847` | no | 1.0.0 |
| W2-FAC-A:L4 | Wave2/W2-FAC-A/lemmas/L4_assembly.md:19-27 | no | `2d513188b824764323e0249104721c9a9cf1bb71e668ae09ebb35f1b18b717c9` | `2d513188b824764323e0249104721c9a9cf1bb71e668ae09ebb35f1b18b717c9` | no | 1.0.0 |
| W2-FAC-A:L5 | Wave2/W2-FAC-A/lemmas/L5_random_instances.md:51-53 | no | `bd15bb32c0c73c25cf190363072391bf0ab6bb1f909cf86c17cd45df52449292` | `bd15bb32c0c73c25cf190363072391bf0ab6bb1f909cf86c17cd45df52449292` | no | 1.0.0 |
| W2-FAC-A:Lemma-kappa | Wave2/W2-FAC-A/lemmas/L5_random_instances.md:63-65 | no | `dd0ca00da03eefeb7e891392d5ccc2349aef12ae860378d4a7e7c12cd27a965c` | `dd0ca00da03eefeb7e891392d5ccc2349aef12ae860378d4a7e7c12cd27a965c` | no | 1.0.0 |
| **W2-FAC-A:Prop-F-FAC** | Wave2/W2-FAC-A/lemmas/L7_delivery.md:22-24 | YES | `121f77a08b76663ab5dac32044d3d1023927b0d7728baf8938a13c458a2f02dc` | `c6def222adebed9241753dfb596a41ef2eceb72bed35e86169b985d535f30d96` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| **W2-FAC-B:Thm-FAC-CS** | Wave2/W2-FAC-B/STATEMENT.md:105-134 | YES | `bc18ab1a503b117a7dd715d0a1d6a4d1686725bbf55c3850f188ad9180b29616` | `fed642ffa82905d923d5526ff388cd6d8f286af043f07fd6edd01c00a76f891c` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-B:Thm-FAC-CS(C1-M) | Wave2/W2-FAC-B/STATEMENT.md:107-109 | no | `3d5fc3d413d60a9aa161770ad5b681575193ee8ebaad1b96175d76756c286299` | `3d5fc3d413d60a9aa161770ad5b681575193ee8ebaad1b96175d76756c286299` | no | 1.0.2 |
| W2-FAC-B:L1 | Wave2/W2-FAC-B/lemmas/L1_cs_reduction.md:59-65 | no | `c8058ad3a9afc4b8ac4b6ee8025711feeadb7ed6ab1e3b25d7adfe169c271f28` | `c8058ad3a9afc4b8ac4b6ee8025711feeadb7ed6ab1e3b25d7adfe169c271f28` | no | 1.0.0 |
| W2-FAC-B:L2 | Wave2/W2-FAC-B/lemmas/L2_start.md:69-70 | no | `61e76c66855ffdde9536fec154044eb4287fd8a525616360612f0ccdfee85c2d` | `61e76c66855ffdde9536fec154044eb4287fd8a525616360612f0ccdfee85c2d` | no | 1.0.0 |
| W2-FAC-B:L3 | Wave2/W2-FAC-B/lemmas/L3_event.md:40-40 | no | `aec47061312eaded2b3ae785bf2bcfbc81c042292b6374e26057196733c8d1fc` | `aec47061312eaded2b3ae785bf2bcfbc81c042292b6374e26057196733c8d1fc` | no | 1.0.0 |
| W2-FAC-B:L4 | Wave2/W2-FAC-B/lemmas/L4_path.md:13-19 | no | `0b4a48ce60d8e6275158144f03c852bdaa097136d186f3dad6197762de00d63e` | `0b4a48ce60d8e6275158144f03c852bdaa097136d186f3dad6197762de00d63e` | no | 1.0.0 |
| **W2-FAC-B:L5** | Wave2/W2-FAC-B/lemmas/L5_assembly.md:44-45 | no | `1e2585eaa8c63ab466b46dc3f7d97c4200d85f7a6b83b95dbaed95593cc77291` | `1e2585eaa8c63ab466b46dc3f7d97c4200d85f7a6b83b95dbaed95593cc77291` | no | 1.0.0 (hash unchanged; recorder edits short/notes) |
| W2-FAC-PK:P1 | Wave2/W2-FAC-PK/STATEMENT.md:59-62 | no | `542af5cff8a9cc46b0b53d8a3bffa730dbf891e5717a80a4c9c23c41998bd989` | `542af5cff8a9cc46b0b53d8a3bffa730dbf891e5717a80a4c9c23c41998bd989` | no | 1.0.0 |
| W2-FAC-PK:Thm-NEG | Wave2/W2-FAC-PK/STATEMENT.md:63-68 | no | `0453695573daf56caaed348ee7fe92c355488501e3fb9fe4f5a9c80e35fc0abb` | `0453695573daf56caaed348ee7fe92c355488501e3fb9fe4f5a9c80e35fc0abb` | no | 1.0.0 |
| W2-FAC-PK:Thm-PATH | Wave2/W2-FAC-PK/STATEMENT.md:69-72 | no | `cdf6cb8b62e7d3d7eacfcaeb22b1679c6ddf60a3c1af9a3d9c7cbd66a466ae80` | `cdf6cb8b62e7d3d7eacfcaeb22b1679c6ddf60a3c1af9a3d9c7cbd66a466ae80` | no | 1.0.0 |
| **W2-FAC-PK:Thm-FAC-PK** | Wave2/W2-FAC-PK/STATEMENT.md:73-87 | YES | `534f50a23b0714cf1061f7495e471645b02d54d0e43a7cb050473d13968edd93` | `af1065d233bd65a0e1e6a8b4ef68f01d815b0f46ee0e012065891c66fefe28d9` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-PK:P5 | Wave2/W2-FAC-PK/STATEMENT.md:88-95 | no | `8e5070857a8d1078a877ba4ed5268a2f0dbe124b2e45c4e6bc9df48a7feb3a5c` | `8e5070857a8d1078a877ba4ed5268a2f0dbe124b2e45c4e6bc9df48a7feb3a5c` | no | 1.0.0 |
| W2-FAC-PK:P6 | Wave2/W2-FAC-PK/STATEMENT.md:96-100 | no | `e693141f0e389c28c0d494a0c325cad7e1e58f19b5c528ae972ba61b86e7d1b7` | `e693141f0e389c28c0d494a0c325cad7e1e58f19b5c528ae972ba61b86e7d1b7` | no | 1.0.0 |
| W2-FAC-PK:L0 | Wave2/W2-FAC-PK/lemmas/L0_imports.md:11-41 | no | `f92743a872fd9e863303cc64a280e5a133fde04c292a221d8e175d6443217589` | `f92743a872fd9e863303cc64a280e5a133fde04c292a221d8e175d6443217589` | no | 1.0.0 |
| **W2-FAC-S5:Thm-FAC-BCS-R** | Wave2/W2-FAC-S5/STATEMENT.md:112-124 | YES | `be5f94f49a25f409db0788e48f4f3f36eaab24f1042d2b20bad5f047378f0eaf` | `5b77c2d670ba198cba948ce3c3e37ff6cd33ac57d3bfcc26221590c19a4bc005` | **YES** | 1.0.1 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-S5:KL | Wave2/W2-FAC-S5/STATEMENT.md:125-128 | no | `af94d02ec3df0c4a72267413c4b69120e746ba42d8b4e2774284f22dc0ad75e6` | `af94d02ec3df0c4a72267413c4b69120e746ba42d8b4e2774284f22dc0ad75e6` | no | 1.0.1 |
| W2-FAC-S5:L1 | Wave2/W2-FAC-S5/lemmas/L1_bcs_reduction.md:69-101 | no | `65fa6d1124835ef772ac244e9c2b79816def18a84c3b8a13bcb2d876b291f3a4` | `65fa6d1124835ef772ac244e9c2b79816def18a84c3b8a13bcb2d876b291f3a4` | no | 1.0.2 |
| W2-FAC-S5:L2 | Wave2/W2-FAC-S5/lemmas/L2_start.md:54-55 | no | `923c31747b3b318abab4b1618bb3fe3cadd586e54ffcd8fc794b5ae323e35b08` | `923c31747b3b318abab4b1618bb3fe3cadd586e54ffcd8fc794b5ae323e35b08` | no | 1.0.0 |
| W2-FAC-S5:L3 | Wave2/W2-FAC-S5/lemmas/L3_event.md:19-19 | no | `7c61ea2baee3d62f58d6b0c0a0f345dce92284ef5f99248d0e30077b2e43ca8a` | `7c61ea2baee3d62f58d6b0c0a0f345dce92284ef5f99248d0e30077b2e43ca8a` | no | 1.0.0 |
| W2-FAC-S5:L4 | Wave2/W2-FAC-S5/lemmas/L4_path.md:16-23 | no | `5ee58cdf3844c18e5ff2b16e0b46f6c69130e2c1481154da00bf88a7626b0be5` | `5ee58cdf3844c18e5ff2b16e0b46f6c69130e2c1481154da00bf88a7626b0be5` | no | 1.0.0 |
| **W2-FAC-S5:L5** | Wave2/W2-FAC-S5/lemmas/L5_assembly.md:33-37 | no | `233b30926a2644bf68d97fcd6caeb33c3a586544cbbbfe221bba1ba9bbbf6c6c` | `233b30926a2644bf68d97fcd6caeb33c3a586544cbbbfe221bba1ba9bbbf6c6c` | no | 1.0.0 (hash unchanged; recorder edits short/notes) |
| W2-FAC-S5F:C1 | Wave2/W2-FAC-S5F/STATEMENT.md:76-77 | no | `7abae52eaf06bab184a158d14a87d0d1be9fd34193239a8bc9336a5b7e4f3506` | `7abae52eaf06bab184a158d14a87d0d1be9fd34193239a8bc9336a5b7e4f3506` | no | 1.0.0 |
| W2-FAC-S5F:C2 | Wave2/W2-FAC-S5F/STATEMENT.md:78-87 | no | `ee5aa9c8e6376345fb085c284ab28fd62eb78384c9a92706ae43478bd5a3ffe3` | `ee5aa9c8e6376345fb085c284ab28fd62eb78384c9a92706ae43478bd5a3ffe3` | no | 1.0.0 |
| W2-FAC-S5F:C3 | Wave2/W2-FAC-S5F/STATEMENT.md:88-95 | no | `6c010af483ac1ecf0f2650f73c285068221ee2c2600479283b45e54bf67a67b4` | `6c010af483ac1ecf0f2650f73c285068221ee2c2600479283b45e54bf67a67b4` | no | 1.0.0 |
| W2-FAC-S5F:C4 | Wave2/W2-FAC-S5F/STATEMENT.md:96-99 | no | `349ad4cb08a31af5b130965243d9a98ac9a79dae4620011cb4ffbe0e2b6f8c5f` | `349ad4cb08a31af5b130965243d9a98ac9a79dae4620011cb4ffbe0e2b6f8c5f` | no | 1.0.0 |
| **W2-FAC-X:Thm-FAC-CS-iid** | Wave2/W2-FAC-X/STATEMENT.md:76-95 | YES | `b078d360c8a9178aaeb64cb060978ac559069df089f27f6cf043a85a5805b520` | `b398e6b70e2ec2c14260d9917b6792fefbcc5b1bc09bbb0b86a44f08215c5ed9` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-X:X1 | Wave2/W2-FAC-X/lemmas/X1_representation.md:15-24 | no | `4450f6e255094e28ccab3472c95a0753c6fc4cf4b0cae0808ae770f2c9281349` | `4450f6e255094e28ccab3472c95a0753c6fc4cf4b0cae0808ae770f2c9281349` | no | 1.0.0 |
| W2-FAC-X:X2 | Wave2/W2-FAC-X/lemmas/X2_perturbation.md:69-71 | no | `f2a138f42fc7adaa90c2eb1ffca0c895b51eb707f757ea9962b3e09cf1c4595b` | `f2a138f42fc7adaa90c2eb1ffca0c895b51eb707f757ea9962b3e09cf1c4595b` | no | 1.0.0 |
| W2-FAC-X:X5 | Wave2/W2-FAC-X/lemmas/X5_start.md:63-65 | no | `5bfb6d62a8585a442fa5b1d8b76a6c291ee42744930db6d83c9793d41dc9db26` | `5bfb6d62a8585a442fa5b1d8b76a6c291ee42744930db6d83c9793d41dc9db26` | no | 1.0.0 |
| W2-FAC-X:X6 | Wave2/W2-FAC-X/lemmas/X6_assembly.md:48-50 | no | `3bded2b49829437d4e47186d00c2f4c40633c790910fab273ef2f3c8274d51f9` | `3bded2b49829437d4e47186d00c2f4c40633c790910fab273ef2f3c8274d51f9` | no | 1.0.0 |
| **W2-FAC-X:Thm-FAC-GL** | Wave2/W2-FAC-X/STATEMENT_T2.md:49-62 | YES | `7eddce31a0a33d7e1ef486336e9f4d0f0bf66677a0afc5e042ccbdd59f5d0b7a` | `c4d9487488ed920421a5f1b918b07b838ec5535078d166879a7f8728e23a5e73` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-X:Cor-FAC-NCS | Wave2/W2-FAC-X/STATEMENT_T2.md:64-69 | no | `e670025355521fffd7e59c250d05dc71badc0a4c076789b39b54b60df82c455a` | `e670025355521fffd7e59c250d05dc71badc0a4c076789b39b54b60df82c455a` | no | 1.0.0 |
| W2-FAC-X:X7 | Wave2/W2-FAC-X/lemmas/X7_near_cs_loadings.md:19-20 | no | `a41cc99b2d31040599476159a8c91343f4f15e24a9409a2e34e5a4c837e45362` | `a41cc99b2d31040599476159a8c91343f4f15e24a9409a2e34e5a4c837e45362` | no | 1.0.0 |
| W2-FAC-X:X8 | Wave2/W2-FAC-X/lemmas/X8_start_general.md:17-19 | no | `7ff27d8464c7f4d580a5feef69eac0af2442a351058d3c11272deb9eb4ef9ab5` | `7ff27d8464c7f4d580a5feef69eac0af2442a351058d3c11272deb9eb4ef9ab5` | no | 1.0.0 |
| **W2-FAC-X:X10** | Wave2/W2-FAC-X/lemmas/X10_assembly_T2.md:1-1 | no | `33bdac8d0d40e0fdc9f02c5b86e66fbaa503b5bd0dc3d40e86a7e3b82c2596ec` | `8c32f2d0102a52916ca049f54bfc8747fe7751a93f12b0f7145ddef7cbd062a9` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-XA:X1 | Wave2/W2-FAC-XA/STATEMENT.md:74-75 | no | `bf386d71086ac7ac6051b69b15a4d7e21462aa5d0326c564878ecd9e4f8a229f` | `bf386d71086ac7ac6051b69b15a4d7e21462aa5d0326c564878ecd9e4f8a229f` | no | 1.0.0 |
| W2-FAC-XA:X2 | Wave2/W2-FAC-XA/STATEMENT.md:76-82 | no | `b6ed3a6385ae9f1ae1f6de293b415ed78c036bdadde425ca24669a897ff5f85e` | `b6ed3a6385ae9f1ae1f6de293b415ed78c036bdadde425ca24669a897ff5f85e` | no | 1.0.0 |
| W2-FAC-XA:X3 | Wave2/W2-FAC-XA/STATEMENT.md:83-84 | no | `ef504dc6837437f6b320f9dcb893e04d30d3a2b775f4aabf0b5314d823bf107a` | `ef504dc6837437f6b320f9dcb893e04d30d3a2b775f4aabf0b5314d823bf107a` | no | 1.0.0 |
| **W2-FAC-XA:X4** | Wave2/W2-FAC-XA/STATEMENT.md:85-86 | YES | `92e83ce73b6795812d193eb1209dd935762e304509a1a76e05cd419736debe80` | `dcae8987f2f75961d183d712ee833256d382e17328d1e13d37cab2de82a72e5b` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-LOC2:L0' | Wave2/W2-LOC2/STATEMENT.md:35-41 | no | `7956bcff9bebe2bf37b3c0a83c85f088dd9566a246f1ab601b8fae74a9abc252` | `7956bcff9bebe2bf37b3c0a83c85f088dd9566a246f1ab601b8fae74a9abc252` | no | 1.0.0 |
| W2-LOC2:NA-R | Wave2/W2-LOC2/STATEMENT.md:43-59 | no | `43e09fc4d2d52943c0315a24d19ffd4670f68741a84e4657dcb66c37b586853d` | `43e09fc4d2d52943c0315a24d19ffd4670f68741a84e4657dcb66c37b586853d` | no | 1.0.0 |
| W2-LOC2:PLR | Wave2/W2-LOC2/STATEMENT.md:61-65 | no | `a5ba654eef8233844f74f958cf75572e61790015a7dd0ce444199634efaa2678` | `a5ba654eef8233844f74f958cf75572e61790015a7dd0ce444199634efaa2678` | no | 1.0.0 |
| W2-LOC2:LOC-d | Wave2/W2-LOC2/STATEMENT.md:67-74 | no | `214c61857e6641fce6bcd59369cdd1298eb6ab967e211b45355b3a5291651104` | `214c61857e6641fce6bcd59369cdd1298eb6ab967e211b45355b3a5291651104` | no | 1.0.0 |
| W2-LOC2:LOC-BF | Wave2/W2-LOC2/STATEMENT.md:76-85 | no | `a8a53bc14734c4dea5d48867aaa169bb0f20aace3704e6b32dca9567a502eb07` | `a8a53bc14734c4dea5d48867aaa169bb0f20aace3704e6b32dca9567a502eb07` | no | 1.0.0 |
| W2-LOC2:Thm-Poly | Wave2/W2-LOC2/STATEMENT.md:87-93 | no | `52c125364358a8279a6b7ed7141a8cf423e7d92a8958be1e0a28c806c945f63d` | `52c125364358a8279a6b7ed7141a8cf423e7d92a8958be1e0a28c806c945f63d` | no | 1.0.1 |
| **W2-LOC2:F-LOC2** | Wave2/W2-LOC2/STATEMENT.md:100-102 | YES | `cc1dcf3b5a1baeab92beb2ffe6831902e3aec61972ef857e8fd4cc486784f304` | `afdcd02e7dc4d34b09c6599d520efae4df57bdf606db7d159cc7b0e126959642` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-UNI:UNI-P | Wave2/W2-UNI/STATEMENT.md:87-91 | no | `164549c462785fe5e160525a18b6fd4f594f3a91e34164aea6b65a6d53f4f351` | `164549c462785fe5e160525a18b6fd4f594f3a91e34164aea6b65a6d53f4f351` | no | 1.0.0 |
| W2-UNI:CT_M | Wave2/W2-UNI/lemmas/L1_metric.md:33-42 | no | `65487210be55abb4895cceb42c4caf8e2f2fc14391576e50876615c9ebfd028b` | `65487210be55abb4895cceb42c4caf8e2f2fc14391576e50876615c9ebfd028b` | no | 1.1.0 |
| W2-UNI:CD_M | Wave2/W2-UNI/lemmas/L1_metric.md:71-77 | no | `4f9b9d59e08fe912d3b6bddd4fd12253f64785f414d3845afe8d4a598cd6d2b2` | `4f9b9d59e08fe912d3b6bddd4fd12253f64785f414d3845afe8d4a598cd6d2b2` | no | 1.1.0 |
| W2-UNI:RB_M | Wave2/W2-UNI/lemmas/L1_metric.md:92-93 | no | `58d371d71f5501db0be63d1d86205d85eeb0036865213d4c70b0469579642ae0` | `58d371d71f5501db0be63d1d86205d85eeb0036865213d4c70b0469579642ae0` | no | 1.1.0 |
| W2-UNI:TAIL_M | Wave2/W2-UNI/lemmas/L1_metric.md:105-108 | no | `9343c5ed31b0a3e67b0455ab889ef345141ce785b1aaf1ae9114376f46850f95` | `9343c5ed31b0a3e67b0455ab889ef345141ce785b1aaf1ae9114376f46850f95` | no | 1.1.0 |
| W2-UNI:LOCL | Wave2/W2-UNI/lemmas/L1_metric.md:123-133 | no | `977c4735a40d98ea486af0a661a2f9d3364aba24440ee4dd439771454fba23f1` | `977c4735a40d98ea486af0a661a2f9d3364aba24440ee4dd439771454fba23f1` | no | 1.1.0 |
| W2-UNI:SC_M | Wave2/W2-UNI/lemmas/L1_metric.md:156-158 | no | `0a5272d9b5fa92509d40dde2f429d35d98633d347cfa7b1710d800d5ce015b67` | `0a5272d9b5fa92509d40dde2f429d35d98633d347cfa7b1710d800d5ce015b67` | no | 1.1.0 |
| **W2-UNI:UNI-0** | Wave2/W2-UNI/STATEMENT.md:103-110 | YES | `f1c1d1aad05f97177f5e068c94f43470fe03dd60445e1fa87e0638a91550a1d5` | `e16cf1d1a03af3b3cd6964d076c462b25656239a7026d389b84c5541d2991c9d` | **YES** | 1.1.2 → 2.0.0 (WEAKER, major = narrow) |
| W2-UNI:U-LOC | Wave2/W2-UNI/STATEMENT.md:155-169 | no | `53e4720e3b5d0700b213f81944ef57967c649d4a899b002a2e54f25910319b92` | `53e4720e3b5d0700b213f81944ef57967c649d4a899b002a2e54f25910319b92` | no | 1.1.0 |
| **W2-UNI:UNI-1** | Wave2/W2-UNI/STATEMENT.md:112-131 | YES | `f28630293ab979ac06691717df635376c415d879af1f5b27f5b18c9b9fdf971c` | `a0bffc530d0d4937bfbd6f77c7523baf0fd410adf3b329da30890c8ab02705df` | **YES** | 2.0.0 → 3.0.0 (WEAKER, major = narrow) |
| W2-UNI:U-LOC-Cor | Wave2/W2-UNI/lemmas/L3_ULOC.md:107-126 | no | `60404520242be51a0511abca8f3166fbbd507669dc74e25407bb483fbfd8c9b7` | `60404520242be51a0511abca8f3166fbbd507669dc74e25407bb483fbfd8c9b7` | no | 1.0.0 |
| W2-FAC-S5:L1.L1.1 | Wave2/W2-FAC-S5/lemmas/L1_bcs_reduction.md:22-27 | no | `ba27cd73359b14c5171037fbb5dbcedab7c179f889a013abaab5d4806321fc69` | `ba27cd73359b14c5171037fbb5dbcedab7c179f889a013abaab5d4806321fc69` | no | 1.0.0 |
| W2-FAC-S5:L1.L1.2 | Wave2/W2-FAC-S5/lemmas/L1_bcs_reduction.md:29-42 | no | `672468e202bd8eb2c2b8bf2ce2b97d8a82df81df3140415a3d91b4efe45a4b4b` | `672468e202bd8eb2c2b8bf2ce2b97d8a82df81df3140415a3d91b4efe45a4b4b` | no | 1.0.0 |
| W2-FAC-S5:L1.L1.3 | Wave2/W2-FAC-S5/lemmas/L1_bcs_reduction.md:44-67 | no | `22dad68fca43f8e80b64211e4981f37ae73f5777d02e942976e8f26d3f5835fb` | `22dad68fca43f8e80b64211e4981f37ae73f5777d02e942976e8f26d3f5835fb` | no | 1.0.0 |
| W2-FAC-S5:L1.L1.4 | Wave2/W2-FAC-S5/lemmas/L1_bcs_reduction.md:69-101 | no | `6fea9da8f2cb9814bfc7c086248ab32674b8dd9c4593226242efc793a46f63a3` | `6fea9da8f2cb9814bfc7c086248ab32674b8dd9c4593226242efc793a46f63a3` | no | 1.0.0 |
| W2-FAC-S5:L5.C3-R | Wave2/W2-FAC-S5/lemmas/L5_assembly.md:33-36 | no | `9bac3c233b66271c490c894ae37aee50ad10749a587d3761d8e496e4032e7f8a` | `9bac3c233b66271c490c894ae37aee50ad10749a587d3761d8e496e4032e7f8a` | no | 1.0.0 |
| **W2-FAC-S5:L5.C4-R** | Wave2/W2-FAC-S5/lemmas/L5_assembly.md:39-43 | YES | `a05be24a7cc9986445aa1017fdd4202ae4f0303128df136524382866aa629745` | `78358e25c309282854e5b1170ef80b27c147b7ae37068874087c52c3829bfe5c` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-X:X1.X1.1 | Wave2/W2-FAC-X/lemmas/X1_representation.md:22-24 | no | `516d5e50dd044bb3e6695b21d01ac3bc7b1b5713f4c19a2797d3b4b0c5754974` | `516d5e50dd044bb3e6695b21d01ac3bc7b1b5713f4c19a2797d3b4b0c5754974` | no | 1.0.0 |
| W2-FAC-X:X1.X1.2 | Wave2/W2-FAC-X/lemmas/X1_representation.md:51-53 | no | `96d0a2d00c6172826b9032af8fb3fdb93e478fff45d66c312e115b26023f52a8` | `96d0a2d00c6172826b9032af8fb3fdb93e478fff45d66c312e115b26023f52a8` | no | 1.0.0 |
| W2-FAC-X:X1.X1.3 | Wave2/W2-FAC-X/lemmas/X1_representation.md:66-67 | no | `5913fc6baa562df753cd82aed8a6f2202a21b3e397251ee6fd77c6ad6a79a57d` | `5913fc6baa562df753cd82aed8a6f2202a21b3e397251ee6fd77c6ad6a79a57d` | no | 1.0.0 |
| W2-FAC-X:X6.X6.3 | Wave2/W2-FAC-X/lemmas/X6_assembly.md:48-50 | no | `1b96d8e5b2884ad1fb8fc0cc8339f8951d4b7385760dd745afe77fc33d142453` | `1b96d8e5b2884ad1fb8fc0cc8339f8951d4b7385760dd745afe77fc33d142453` | no | 1.0.0 |
| W2-FAC-X:X6.X6.4 | Wave2/W2-FAC-X/lemmas/X6_assembly.md:58-61 | no | `3b79b77256f4bb0b36aece89e18f37b7ac1d919ce2ff086a671b3755711839f4` | `3b79b77256f4bb0b36aece89e18f37b7ac1d919ce2ff086a671b3755711839f4` | no | 1.0.0 |
| W2-LOC2:PLR.C-i | Wave2/W2-LOC2/STATEMENT.md:61-63 | no | `ec66bc78c62b7e18100aed2a42afb7256122b813d6c35511c073f86d29cb59b8` | `ec66bc78c62b7e18100aed2a42afb7256122b813d6c35511c073f86d29cb59b8` | no | 1.0.0 |
| W2-LOC2:PLR.C-ii | Wave2/W2-LOC2/STATEMENT.md:63-65 | no | `a5c25331163f046f751b30ab0d16224b2ab55c7bbf23be44b11d075bbb986eb8` | `a5c25331163f046f751b30ab0d16224b2ab55c7bbf23be44b11d075bbb986eb8` | no | 1.0.0 |
| **W2-LOC2:F-LOC2.exp** | Wave2/W2-LOC2/STATEMENT.md:100-102 | YES | `fce4ba02622dd684a2089a4b14cac1af2556172ece5f85d1be35a93014e09552` | `2770153f28373057ca77e632dc35351b164fd0596239dff2dec434e9a81c4388` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| **W2-LOC2:F-LOC2.poly** | Wave2/W2-LOC2/STATEMENT.md:100-102 | YES | `33b7bbed028dd15ff5fa5a87a4cc541db3f021e140440a160ba146da163f4c3e` | `35e6ae8fc8637ecc31a51aab6fcd5ccf77251c26a00e9b7970726f6189235229` | **YES** | 1.0.0 → 2.0.0 (WEAKER, major = narrow) |
| W2-FAC-A:L1.Cor-U | Wave2/W2-FAC-A/lemmas/L1_uniform_add.md:149-154 | no | `d49a18cffa2f89c69b91294e16d045e91b2f8cfca9372dcf5d905aa973b5b74c` | `d49a18cffa2f89c69b91294e16d045e91b2f8cfca9372dcf5d905aa973b5b74c` | no | 1.0.0 |
| W2-FAC-B:L1.L1.3 | Wave2/W2-FAC-B/lemmas/L1_cs_reduction.md:59-65 | no | `c8058ad3a9afc4b8ac4b6ee8025711feeadb7ed6ab1e3b25d7adfe169c271f28` | `c8058ad3a9afc4b8ac4b6ee8025711feeadb7ed6ab1e3b25d7adfe169c271f28` | no | 1.0.0 |

## B. Every cite `touched-file:a-b` in claims.tsv, fragments/*.tsv, assumptions.tsv (any column)
A cite whose text changes is listed with its referrer; none moves. Changed cites are all inside the narrowed lines of the batch rows or the s7 erratum line; the `fragments/splits/s{1,2}.tsv` `repoint`/`part` rows use them as evidence pointers and still point at the same statement.

| cited span | text changed? | cited by |
|---|---|---|
| `Wave1C/C-DLV/STATEMENT.md:11-20` | same | c2_w1c_a.tsv:C-DLV:O, c2_w1c_a.tsv:C-DLV:P1-Inventory, claims.tsv:C-DLV:O, claims.tsv:C-DLV:P1-Inventory |
| `Wave1C/C-DLV/STATEMENT.md:11-46` | same | c2_w1c_a.tsv:C-DLV:C1-CondDelivery, c2_w1c_a.tsv:C-DLV:Cor-Dp, c2_w1c_a.tsv:C-DLV:Prop-F, c2_w1c_a.tsv:C-DLV:Target-T, c2_w1c_a.tsv:C-DLV:Thm-D, claims.tsv:C-DLV:C1-CondDelivery, claims.tsv:C-DLV:Cor-Dp, claims.tsv:C-DLV:Prop-F, claims.tsv:C-DLV:Target-T, claims.tsv:C-DLV:Thm-D |
| `Wave1C/C-DLV/STATEMENT.md:21-46` | same | c2_w1c_a.tsv:C-DLV:Cor-R, c2_w1c_a.tsv:C-DLV:L1-R, claims.tsv:C-DLV:Cor-R, claims.tsv:C-DLV:L1-R |
| `Wave1C/C-DLV/STATEMENT.md:68-69` | same | c2_w1c_a.tsv:C-DLV:O, claims.tsv:C-DLV:O |
| `Wave1C/FINAL/sections/s7_impl.tex:36-43` | **CHANGED** | c3_w1c_b.tsv:W1C-FINAL:Lemma-CAP, claims.tsv:W1C-FINAL:Lemma-CAP |
| `Wave1C/FINAL/sections/s7_impl.tex:45-56` | same | claims.tsv:W1C-FINAL:Lemma-CAP |
| `Wave1C/FINAL/sections/s7_impl.tex:58-60` | same | c3_w1c_b.tsv:W1C-FINAL:Lemma-CAP |
| `Wave1C/FINAL/sections/s7_impl.tex:64` | same | claims.tsv:W1C-FINAL:Lemma-CAP |
| `Wave1C/HQ_AUDIT/A2_propF_GROW.md:1` | same | claims.tsv:HQ_AUDIT-W1C:A2 |
| `Wave1C/HQ_AUDIT/A2_propF_GROW.md:25` | same | c3_w1c_b.tsv:HQ_AUDIT-W1C:A2 |
| `Wave1C/HQ_AUDIT/A2_propF_GROW.md:5-35` | **CHANGED** | c3_w1c_b.tsv:HQ_AUDIT-W1C:A2 |
| `Wave1C/HQ_AUDIT/A2_propF_GROW.md:9` | same | c3_w1c_b.tsv:HQ_AUDIT-W1C:A2 |
| `Wave1C/HQ_AUDIT/A3_check_A2.md:5` | **CHANGED** | claims.tsv:HQ_AUDIT-W1C:A3 |
| `Wave2/W2-FAC-A/STATEMENT.md:102` | same | c4_w2_fac.tsv:W2-FAC-A:Thm-FAC-L |
| `Wave2/W2-FAC-A/STATEMENT.md:105` | same | assumptions.tsv:P:ADD-BOUND |
| `Wave2/W2-FAC-A/STATEMENT.md:128` | same | assumptions.tsv:A:DELIVERY-ALLOC |
| `Wave2/W2-FAC-A/STATEMENT.md:136` | same | sharpness.tsv:W2-FAC-A:Prop-F-FAC, sharpness.tsv:W2-FAC-A:Thm-FAC-L |
| `Wave2/W2-FAC-A/STATEMENT.md:154-159` | same | s1.tsv:repoint |
| `Wave2/W2-FAC-A/STATEMENT.md:43-59` | same | c4_w2_fac.tsv:W2-FAC-A:Thm-FAC-L, claims.tsv:W2-FAC-A:Thm-FAC-L |
| `Wave2/W2-FAC-A/STATEMENT.md:44-44` | same | c4_w2_fac.tsv:W2-FAC-A:Prop-SHARP, claims.tsv:W2-FAC-A:Prop-SHARP |
| `Wave2/W2-FAC-A/STATEMENT.md:46-48` | same | c4_w2_fac.tsv:W2-FAC-A:L1, c4_w2_fac.tsv:W2-FAC-A:L2, c4_w2_fac.tsv:W2-FAC-A:L4, c4_w2_fac.tsv:W2-FAC-A:Prop-SHARP, claims.tsv:W2-FAC-A:L1, claims.tsv:W2-FAC-A:L1.Cor-U, claims.tsv:W2-FAC-A:L2, claims.tsv:W2-FAC-A:L4, claims.tsv:W2-FAC-A:Prop-SHARP, s1.tsv:part |
| `Wave2/W2-FAC-A/STATEMENT.md:49-51` | same | c4_w2_fac.tsv:W2-FAC-A:L5, claims.tsv:W2-FAC-A:L5 |
| `Wave2/W2-FAC-A/STATEMENT.md:52-59` | same | c4_w2_fac.tsv:W2-FAC-A:L4, claims.tsv:W2-FAC-A:L4 |
| `Wave2/W2-FAC-A/STATEMENT.md:57-57` | same | c4_w2_fac.tsv:W2-FAC-A:L3.1, c4_w2_fac.tsv:W2-FAC-A:Prop-SHARP, claims.tsv:W2-FAC-A:L3.1, claims.tsv:W2-FAC-A:Prop-SHARP |
| `Wave2/W2-FAC-A/STATEMENT.md:58-58` | same | c4_w2_fac.tsv:W2-FAC-A:L3.2, claims.tsv:W2-FAC-A:L3.2 |
| `Wave2/W2-FAC-A/STATEMENT.md:58-59` | same | c4_w2_fac.tsv:W2-FAC-A:L2, claims.tsv:W2-FAC-A:L2 |
| `Wave2/W2-FAC-A/STATEMENT.md:62` | same | assumptions.tsv:A:INST-FACTOR |
| `Wave2/W2-FAC-A/STATEMENT.md:63-69` | same | c4_w2_fac.tsv:W2-FAC-A:L1, claims.tsv:W2-FAC-A:L1, claims.tsv:W2-FAC-A:L1.Cor-U, s1.tsv:part |
| `Wave2/W2-FAC-A/STATEMENT.md:63-71` | same | c4_w2_fac.tsv:W2-FAC-A:Thm-FAC-L, claims.tsv:W2-FAC-A:Thm-FAC-L |
| `Wave2/W2-FAC-A/STATEMENT.md:65-67` | same | c4_w2_fac.tsv:W2-FAC-A:Lemma-kappa, claims.tsv:W2-FAC-A:Lemma-kappa |
| `Wave2/W2-FAC-A/STATEMENT.md:86-95` | same | c4_w2_fac.tsv:W2-FAC-A:L4, claims.tsv:W2-FAC-A:L4 |
| `Wave2/W2-FAC-A/STATEMENT.md:86-99` | same | c4_w2_fac.tsv:W2-FAC-A:Thm-FAC-L, claims.tsv:W2-FAC-A:Thm-FAC-L |
| `Wave2/W2-FAC-A/STATEMENT.md:90` | same | assumptions.tsv:A:EXACT-GRAM, assumptions.tsv:A:GRAM-OP-BOUND |
| `Wave2/W2-FAC-A/STATEMENT.md:90-91` | same | c4_w2_fac.tsv:W2-FAC-A:L1, claims.tsv:W2-FAC-A:L1, claims.tsv:W2-FAC-A:L1.Cor-U, s1.tsv:part |
| `Wave2/W2-FAC-A/STATEMENT.md:92` | same | assumptions.tsv:A:P-ALPHA0 |
| `Wave2/W2-FAC-A/STATEMENT.md:94-100` | same | c6_w2_misc.tsv:W2-UNI:UNI-1, c7_w2uni_closed.tsv:W2-UNI:UNI-1, claims.tsv:W2-UNI:UNI-1 |
| `Wave2/W2-FAC-A/STATEMENT.md:96-99` | same | c4_w2_fac.tsv:W2-FAC-A:L5, claims.tsv:W2-FAC-A:L5 |
| `Wave2/W2-FAC-A/lemmas/L7_delivery.md:3` | same | claims.tsv:W2-FAC-A:Prop-F-FAC |
| `Wave2/W2-FAC-A/lemmas/L7_delivery.md:35-48` | same | c4_w2_fac.tsv:W2-FAC-A:Prop-F-FAC |
| `Wave2/W2-FAC-A/lemmas/L7_delivery.md:7-20` | same | c4_w2_fac.tsv:W2-FAC-A:Prop-F-FAC, claims.tsv:W2-FAC-A:Prop-F-FAC |
| `Wave2/W2-FAC-B/STATEMENT.md:122` | same | sharpness.tsv:W2-FAC-B:Thm-FAC-CS |
| `Wave2/W2-FAC-B/STATEMENT.md:124` | same | c4_w2_fac.tsv:W2-FAC-B:Thm-FAC-CS |
| `Wave2/W2-FAC-B/STATEMENT.md:127` | same | c4_w2_fac.tsv:W2-FAC-B:Thm-FAC-CS, sharpness.tsv:W2-FAC-B:Thm-FAC-CS |
| `Wave2/W2-FAC-B/STATEMENT.md:39-70` | same | c5_w2_x.tsv:W2-FAC-S5F:C1, c5_w2_x.tsv:W2-FAC-S5F:C2, c5_w2_x.tsv:W2-FAC-S5F:C3, c5_w2_x.tsv:W2-FAC-S5F:C4, claims.tsv:W2-FAC-S5F:C1, claims.tsv:W2-FAC-S5F:C2, claims.tsv:W2-FAC-S5F:C3, claims.tsv:W2-FAC-S5F:C4 |
| `Wave2/W2-FAC-B/STATEMENT.md:45-48` | same | c4_w2_fac.tsv:W2-FAC-B:Thm-FAC-CS, claims.tsv:W2-FAC-B:Thm-FAC-CS |
| `Wave2/W2-FAC-B/STATEMENT.md:53-69` | same | c4_w2_fac.tsv:W2-FAC-B:L5, c4_w2_fac.tsv:W2-FAC-B:Thm-FAC-CS, claims.tsv:W2-FAC-B:L5, claims.tsv:W2-FAC-B:Thm-FAC-CS |
| `Wave2/W2-FAC-B/STATEMENT.md:73` | same | assumptions.tsv:A:INST-CS |
| `Wave2/W2-FAC-B/STATEMENT.md:73-74` | same | c4_w2_fac.tsv:W2-FAC-B:L1, claims.tsv:W2-FAC-B:L1, claims.tsv:W2-FAC-B:L1.L1.3, s1.tsv:part |
| `Wave2/W2-FAC-B/STATEMENT.md:73-78` | same | c4_w2_fac.tsv:W2-FAC-B:L3, c4_w2_fac.tsv:W2-FAC-B:L4, claims.tsv:W2-FAC-B:L3, claims.tsv:W2-FAC-B:L4 |
| `Wave2/W2-FAC-B/STATEMENT.md:73-84` | same | c4_w2_fac.tsv:W2-FAC-B:L2, c4_w2_fac.tsv:W2-FAC-B:L5, c4_w2_fac.tsv:W2-FAC-B:Thm-FAC-CS, c4_w2_fac.tsv:W2-FAC-B:Thm-FAC-CS(C1-M), claims.tsv:W2-FAC-B:L2, claims.tsv:W2-FAC-B:L5, claims.tsv:W2-FAC-B:Thm-FAC-CS, claims.tsv:W2-FAC-B:Thm-FAC-CS(C1-M) |
| `Wave2/W2-FAC-B/STATEMENT.md:75` | same | assumptions.tsv:A:P-HALF-N |
| `Wave2/W2-FAC-B/STATEMENT.md:79` | same | assumptions.tsv:A:FS |
| `Wave2/W2-FAC-B/STATEMENT.md:84` | same | sharpness.tsv:W2-FAC-B:Thm-FAC-CS |
| `Wave2/W2-FAC-B/lemmas/L5_assembly.md:21` | same | s1.tsv:repoint |
| `Wave2/W2-FAC-B/lemmas/L5_assembly.md:3` | same | claims.tsv:W2-FAC-B:L5 |
| `Wave2/W2-FAC-B/lemmas/L5_assembly.md:30-30` | same | c4_w2_fac.tsv:W2-FAC-B:L5, claims.tsv:W2-FAC-B:L5 |
| `Wave2/W2-FAC-B/lemmas/L5_assembly.md:47-48` | same | c4_w2_fac.tsv:W2-FAC-B:Thm-FAC-CS |
| `Wave2/W2-FAC-B/lemmas/L5_assembly.md:6-16` | same | c4_w2_fac.tsv:W2-FAC-B:L5 |
| `Wave2/W2-FAC-PK/STATEMENT.md:37-43` | same | c4_w2_fac.tsv:W2-FAC-PK:P1, c4_w2_fac.tsv:W2-FAC-PK:Thm-FAC-PK, c4_w2_fac.tsv:W2-FAC-PK:Thm-NEG, c4_w2_fac.tsv:W2-FAC-PK:Thm-PATH, claims.tsv:W2-FAC-PK:P1, claims.tsv:W2-FAC-PK:Thm-FAC-PK, claims.tsv:W2-FAC-PK:Thm-NEG, claims.tsv:W2-FAC-PK:Thm-PATH |
| `Wave2/W2-FAC-PK/STATEMENT.md:47-48` | same | c4_w2_fac.tsv:W2-FAC-PK:L0, claims.tsv:W2-FAC-PK:L0 |
| `Wave2/W2-FAC-PK/STATEMENT.md:47-50` | same | c4_w2_fac.tsv:W2-FAC-PK:Thm-FAC-PK, c4_w2_fac.tsv:W2-FAC-PK:Thm-PATH, claims.tsv:W2-FAC-PK:Thm-FAC-PK, claims.tsv:W2-FAC-PK:Thm-PATH |
| `Wave2/W2-FAC-PK/STATEMENT.md:47-54` | same | c4_w2_fac.tsv:W2-FAC-PK:P1, c4_w2_fac.tsv:W2-FAC-PK:Thm-NEG, claims.tsv:W2-FAC-PK:P1, claims.tsv:W2-FAC-PK:Thm-NEG |
| `Wave2/W2-FAC-PK/STATEMENT.md:50` | same | assumptions.tsv:A:PK-REGIME |
| `Wave2/W2-FAC-PK/STATEMENT.md:51` | same | assumptions.tsv:A:PK-NEG-REGIME |
| `Wave2/W2-FAC-PK/STATEMENT.md:59-62` | same | s1.tsv:repoint |
| `Wave2/W2-FAC-PK/STATEMENT.md:60` | same | s1.tsv:repoint |
| `Wave2/W2-FAC-PK/STATEMENT.md:96-100` | same | c4_w2_fac.tsv:W2-FAC-PK:P6 |
| `Wave2/W2-FAC-S5/STATEMENT.md:121-122` | same | s2.tsv:repoint |
| `Wave2/W2-FAC-S5/STATEMENT.md:123-124` | **CHANGED** | s2.tsv:repoint |
| `Wave2/W2-FAC-S5/STATEMENT.md:148` | same | s1.tsv:repoint |
| `Wave2/W2-FAC-S5/STATEMENT.md:51-52` | same | c5_w2_x.tsv:W2-FAC-S5:L1, c5_w2_x.tsv:W2-FAC-S5:L2, c5_w2_x.tsv:W2-FAC-S5:L3, c5_w2_x.tsv:W2-FAC-S5:L4, claims.tsv:W2-FAC-S5:L1, claims.tsv:W2-FAC-S5:L1.L1.1, claims.tsv:W2-FAC-S5:L1.L1.2, claims.tsv:W2-FAC-S5:L1.L1.3, claims.tsv:W2-FAC-S5:L1.L1.4, claims.tsv:W2-FAC-S5:L2, claims.tsv:W2-FAC-S5:L3, claims.tsv:W2-FAC-S5:L4, s2.tsv:part |
| `Wave2/W2-FAC-S5/STATEMENT.md:51-57` | same | c5_w2_x.tsv:W2-FAC-S5:L5, c5_w2_x.tsv:W2-FAC-S5:Thm-FAC-BCS-R, claims.tsv:W2-FAC-S5:L5, claims.tsv:W2-FAC-S5:L5.C3-R, claims.tsv:W2-FAC-S5:L5.C4-R, claims.tsv:W2-FAC-S5:Thm-FAC-BCS-R, s2.tsv:part |
| `Wave2/W2-FAC-S5/STATEMENT.md:61-67` | same | c5_w2_x.tsv:W2-FAC-S5:L1, c5_w2_x.tsv:W2-FAC-S5:L3, c5_w2_x.tsv:W2-FAC-S5:L4, claims.tsv:W2-FAC-S5:L1, claims.tsv:W2-FAC-S5:L1.L1.1, claims.tsv:W2-FAC-S5:L1.L1.2, claims.tsv:W2-FAC-S5:L1.L1.3, claims.tsv:W2-FAC-S5:L1.L1.4, claims.tsv:W2-FAC-S5:L3, claims.tsv:W2-FAC-S5:L4, s2.tsv:part |
| `Wave2/W2-FAC-S5/STATEMENT.md:61-77` | same | c5_w2_x.tsv:W2-FAC-S5:KL, c5_w2_x.tsv:W2-FAC-S5:L2, c5_w2_x.tsv:W2-FAC-S5:L5, c5_w2_x.tsv:W2-FAC-S5:Thm-FAC-BCS-R, claims.tsv:W2-FAC-S5:KL, claims.tsv:W2-FAC-S5:L2, claims.tsv:W2-FAC-S5:L5, claims.tsv:W2-FAC-S5:L5.C3-R, claims.tsv:W2-FAC-S5:L5.C4-R, claims.tsv:W2-FAC-S5:Thm-FAC-BCS-R, s2.tsv:part |
| `Wave2/W2-FAC-S5/STATEMENT.md:81-95` | same | claims.tsv:W2-FAC-S5:KL, claims.tsv:W2-FAC-S5:Thm-FAC-BCS-R |
| `Wave2/W2-FAC-S5/STATEMENT.md:91` | same | s2.tsv:repoint |
| `Wave2/W2-FAC-S5/STATEMENT.md:97-108` | same | c5_w2_x.tsv:W2-FAC-S5:KL, c5_w2_x.tsv:W2-FAC-S5:L5, c5_w2_x.tsv:W2-FAC-S5:Thm-FAC-BCS-R, claims.tsv:W2-FAC-S5:KL, claims.tsv:W2-FAC-S5:L5, claims.tsv:W2-FAC-S5:L5.C3-R, claims.tsv:W2-FAC-S5:L5.C4-R, claims.tsv:W2-FAC-S5:Thm-FAC-BCS-R, s2.tsv:part |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md:15-19` | same | claims.tsv:W2-FAC-S5:L5.C3-R, claims.tsv:W2-FAC-S5:L5.C4-R, s2.tsv:part |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md:17` | same | s2.tsv:repoint |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md:21-31` | same | claims.tsv:W2-FAC-S5:L5.C3-R, claims.tsv:W2-FAC-S5:L5.C4-R, s2.tsv:part |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md:3` | same | claims.tsv:W2-FAC-S5:L5, claims.tsv:W2-FAC-S5:L5.C3-R, claims.tsv:W2-FAC-S5:L5.C4-R, s2.tsv:part |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md:33-36` | same | s2.tsv:part |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md:39-47` | **CHANGED** | s2.tsv:part |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md:48-51` | same | claims.tsv:W2-FAC-S5:L5.C4-R, s2.tsv:part |
| `Wave2/W2-FAC-S5/lemmas/L5_assembly.md:8-13` | same | claims.tsv:W2-FAC-S5:L5.C3-R, claims.tsv:W2-FAC-S5:L5.C4-R, s2.tsv:part |
| `Wave2/W2-FAC-X/STATEMENT.md:36-39` | same | c5_w2_x.tsv:W2-FAC-X:Cor-FAC-NCS, c5_w2_x.tsv:W2-FAC-X:X1, c5_w2_x.tsv:W2-FAC-X:X6, claims.tsv:W2-FAC-X:Cor-FAC-NCS, claims.tsv:W2-FAC-X:X1, claims.tsv:W2-FAC-X:X1.X1.1, claims.tsv:W2-FAC-X:X1.X1.2, claims.tsv:W2-FAC-X:X1.X1.3, claims.tsv:W2-FAC-X:X6, claims.tsv:W2-FAC-X:X6.X6.3, claims.tsv:W2-FAC-X:X6.X6.4, s2.tsv:part |
| `Wave2/W2-FAC-X/STATEMENT.md:36-44` | same | c5_w2_x.tsv:W2-FAC-X:Thm-FAC-CS-iid, claims.tsv:W2-FAC-X:Thm-FAC-CS-iid |
| `Wave2/W2-FAC-X/STATEMENT.md:48-50` | same | c5_w2_x.tsv:W2-FAC-X:X1, claims.tsv:W2-FAC-X:X1, claims.tsv:W2-FAC-X:X1.X1.1, claims.tsv:W2-FAC-X:X1.X1.2, claims.tsv:W2-FAC-X:X1.X1.3, s2.tsv:part |
| `Wave2/W2-FAC-X/STATEMENT.md:48-56` | same | c5_w2_x.tsv:W2-FAC-X:Cor-FAC-NCS, c5_w2_x.tsv:W2-FAC-X:Thm-FAC-CS-iid, c5_w2_x.tsv:W2-FAC-X:X5, c5_w2_x.tsv:W2-FAC-X:X6, c5_w2_x.tsv:W2-FAC-X:X7, claims.tsv:W2-FAC-X:Cor-FAC-NCS, claims.tsv:W2-FAC-X:Thm-FAC-CS-iid, claims.tsv:W2-FAC-X:X5, claims.tsv:W2-FAC-X:X6, claims.tsv:W2-FAC-X:X6.X6.3, claims.tsv:W2-FAC-X:X6.X6.4, claims.tsv:W2-FAC-X:X7, s2.tsv:part |
| `Wave2/W2-FAC-X/STATEMENT.md:49` | same | assumptions.tsv:A:P-HALF |
| `Wave2/W2-FAC-X/STATEMENT.md:60-72` | same | c5_w2_x.tsv:W2-FAC-X:Thm-FAC-CS-iid, claims.tsv:W2-FAC-X:Thm-FAC-CS-iid |
| `Wave2/W2-FAC-X/STATEMENT.md:62-63` | same | s2.tsv:repoint |
| `Wave2/W2-FAC-X/STATEMENT.md:70-72` | same | c5_w2_x.tsv:W2-FAC-X:X2, claims.tsv:W2-FAC-X:X2 |
| `Wave2/W2-FAC-X/STATEMENT.md:90` | same | sharpness.tsv:W2-FAC-X:Thm-FAC-CS-iid |
| `Wave2/W2-FAC-X/STATEMENT.md:99` | same | sharpness.tsv:W2-FAC-X:Thm-FAC-CS-iid |
| `Wave2/W2-FAC-X/STATEMENT_T2.md:22-45` | same | c5_w2_x.tsv:W2-FAC-X:Thm-FAC-GL, claims.tsv:W2-FAC-X:Thm-FAC-GL |
| `Wave2/W2-FAC-X/STATEMENT_T2.md:26-31` | same | c5_w2_x.tsv:W2-FAC-X:Cor-FAC-NCS, c5_w2_x.tsv:W2-FAC-X:X10, c5_w2_x.tsv:W2-FAC-X:X8, claims.tsv:W2-FAC-X:Cor-FAC-NCS, claims.tsv:W2-FAC-X:X10, claims.tsv:W2-FAC-X:X8 |
| `Wave2/W2-FAC-X/STATEMENT_T2.md:35-45` | same | c5_w2_x.tsv:W2-FAC-X:X10, c5_w2_x.tsv:W2-FAC-X:X8, claims.tsv:W2-FAC-X:X10, claims.tsv:W2-FAC-X:X8 |
| `Wave2/W2-FAC-X/STATEMENT_T2.md:49-52` | same | c5_w2_x.tsv:W2-FAC-X:X10, claims.tsv:W2-FAC-X:X10 |
| `Wave2/W2-FAC-X/STATEMENT_T2.md:61-62` | **CHANGED** | c5_w2_x.tsv:W2-FAC-X:X10, claims.tsv:W2-FAC-X:X10 |
| `Wave2/W2-FAC-X/lemmas/X10_assembly_T2.md:17` | same | s2.tsv:repoint |
| `Wave2/W2-FAC-X/lemmas/X10_assembly_T2.md:21` | **CHANGED** | s2.tsv:repoint |
| `Wave2/W2-FAC-X/lemmas/X10_assembly_T2.md:3` | same | claims.tsv:W2-FAC-X:X10 |
| `Wave2/W2-FAC-XA/STATEMENT.md:24-29` | same | c5_w2_x.tsv:W2-FAC-XA:X1, c5_w2_x.tsv:W2-FAC-XA:X2, c5_w2_x.tsv:W2-FAC-XA:X3, c5_w2_x.tsv:W2-FAC-XA:X4, claims.tsv:W2-FAC-XA:X1, claims.tsv:W2-FAC-XA:X2, claims.tsv:W2-FAC-XA:X3, claims.tsv:W2-FAC-XA:X4 |
| `Wave2/W2-FAC-XA/STATEMENT.md:50-72` | same | c5_w2_x.tsv:W2-FAC-XA:X1, c5_w2_x.tsv:W2-FAC-XA:X2, c5_w2_x.tsv:W2-FAC-XA:X3, c5_w2_x.tsv:W2-FAC-XA:X4, claims.tsv:W2-FAC-XA:X1, claims.tsv:W2-FAC-XA:X2, claims.tsv:W2-FAC-XA:X3, claims.tsv:W2-FAC-XA:X4 |
| `Wave2/W2-FAC-XA/STATEMENT.md:9-22` | same | c5_w2_x.tsv:W2-FAC-XA:X1, c5_w2_x.tsv:W2-FAC-XA:X2, c5_w2_x.tsv:W2-FAC-XA:X3, c5_w2_x.tsv:W2-FAC-XA:X4, claims.tsv:W2-FAC-XA:X1, claims.tsv:W2-FAC-XA:X2, claims.tsv:W2-FAC-XA:X3, claims.tsv:W2-FAC-XA:X4 |
| `Wave2/W2-LOC2/STATEMENT.md:19-31` | same | c6_w2_misc.tsv:W2-LOC2:L0', c6_w2_misc.tsv:W2-LOC2:LOC-BF, c6_w2_misc.tsv:W2-LOC2:LOC-d, c6_w2_misc.tsv:W2-LOC2:NA-R, c6_w2_misc.tsv:W2-LOC2:PLR, c6_w2_misc.tsv:W2-LOC2:Thm-Poly, claims.tsv:W2-LOC2:F-LOC2.exp, claims.tsv:W2-LOC2:F-LOC2.poly, claims.tsv:W2-LOC2:L0', claims.tsv:W2-LOC2:LOC-BF, claims.tsv:W2-LOC2:LOC-d, claims.tsv:W2-LOC2:NA-R, claims.tsv:W2-LOC2:PLR, claims.tsv:W2-LOC2:PLR.C-i, claims.tsv:W2-LOC2:PLR.C-ii, claims.tsv:W2-LOC2:Thm-Poly, s2.tsv:part |
| `Wave2/W2-LOC2/STATEMENT.md:35-59` | same | claims.tsv:W2-LOC2:PLR.C-i, claims.tsv:W2-LOC2:PLR.C-ii, s2.tsv:part |
| `Wave2/W2-LOC2/STATEMENT.md:43` | same | assumptions.tsv:A:NA-FRAME |
| `Wave2/W2-LOC2/STATEMENT.md:63-64` | same | claims.tsv:W2-LOC2:PLR.C-ii, s2.tsv:part |
| `Wave2/W2-LOC2/STATEMENT.md:67-85` | same | claims.tsv:W2-LOC2:F-LOC2.exp, s2.tsv:part |
| `Wave2/W2-LOC2/STATEMENT.md:70-71` | same | c6_w2_misc.tsv:W2-LOC2:LOC-BF, c6_w2_misc.tsv:W2-LOC2:Thm-Poly, claims.tsv:W2-LOC2:LOC-BF, claims.tsv:W2-LOC2:Thm-Poly |
| `Wave2/W2-LOC2/STATEMENT.md:87` | same | assumptions.tsv:A:POLY-DECAY |
| `Wave2/W2-LOC2/STATEMENT.md:87-98` | same | claims.tsv:W2-LOC2:F-LOC2.poly, s2.tsv:part, sharpness.tsv:W2-LOC2:Thm-Poly |
| `Wave2/W2-LOC2/STATEMENT.md:91-93` | same | assumptions.tsv:A:RELEVANCE-POLY |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md:14` | same | claims.tsv:W2-LOC2:F-LOC2.exp, s2.tsv:part |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md:14-19` | **CHANGED** | s2.tsv:part |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md:15` | same | claims.tsv:W2-LOC2:F-LOC2.poly, s2.tsv:part |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md:15-19` | **CHANGED** | s2.tsv:part |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md:17-19` | **CHANGED** | claims.tsv:W2-LOC2:F-LOC2.exp, claims.tsv:W2-LOC2:F-LOC2.poly, s2.tsv:part |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md:32` | same | s2.tsv:repoint |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md:7-12` | same | claims.tsv:W2-LOC2:F-LOC2.exp, claims.tsv:W2-LOC2:F-LOC2.poly, s2.tsv:part |
| `Wave2/W2-LOC2/lemmas/L7_delivery.md:7-15` | same | c6_w2_misc.tsv:W2-LOC2:F-LOC2, claims.tsv:W2-LOC2:F-LOC2 |
| `Wave2/W2-UNI/STATEMENT.md:103-110` | **CHANGED** | c7_w2uni_closed.tsv:W2-UNI:UNI-0 |
| `Wave2/W2-UNI/STATEMENT.md:112-131` | **CHANGED** | c7_w2uni_closed.tsv:W2-UNI:UNI-1, s1.tsv:repoint |
| `Wave2/W2-UNI/STATEMENT.md:155-169` | same | c7_w2uni_closed.tsv:W2-UNI:U-LOC |
| `Wave2/W2-UNI/STATEMENT.md:156` | same | s1.tsv:repoint |
| `Wave2/W2-UNI/STATEMENT.md:20-32` | same | c6_w2_misc.tsv:W2-UNI:UNI-0, c6_w2_misc.tsv:W2-UNI:UNI-1, c6_w2_misc.tsv:W2-UNI:UNI-P |
| `Wave2/W2-UNI/STATEMENT.md:22-27` | same | c7_w2uni_closed.tsv:W2-UNI:UNI-P, claims.tsv:W2-UNI:UNI-P |
| `Wave2/W2-UNI/STATEMENT.md:22-34` | same | c7_w2uni_closed.tsv:W2-UNI:UNI-0, c7_w2uni_closed.tsv:W2-UNI:UNI-1, claims.tsv:W2-UNI:UNI-0, claims.tsv:W2-UNI:UNI-1 |
| `Wave2/W2-UNI/STATEMENT.md:38` | same | assumptions.tsv:A:IID-GAUSS-ROWS, sharpness.tsv:W2-UNI:F-UNI |
| `Wave2/W2-UNI/STATEMENT.md:39-43` | same | c6_w2_misc.tsv:W2-UNI:UNI-P |
| `Wave2/W2-UNI/STATEMENT.md:40-45` | same | c7_w2uni_closed.tsv:W2-UNI:UNI-P, claims.tsv:W2-UNI:UNI-P |
| `Wave2/W2-UNI/STATEMENT.md:48-51` | same | c6_w2_misc.tsv:W2-UNI:CD_M, c6_w2_misc.tsv:W2-UNI:CT_M, c6_w2_misc.tsv:W2-UNI:LOCL, c6_w2_misc.tsv:W2-UNI:RB_M, c6_w2_misc.tsv:W2-UNI:SC_M, c6_w2_misc.tsv:W2-UNI:TAIL_M, c6_w2_misc.tsv:W2-UNI:U-LOC, c6_w2_misc.tsv:W2-UNI:UNI-0, c6_w2_misc.tsv:W2-UNI:UNI-1 |
| `Wave2/W2-UNI/STATEMENT.md:50-53` | same | c7_w2uni_closed.tsv:W2-UNI:CD_M, c7_w2uni_closed.tsv:W2-UNI:CT_M, c7_w2uni_closed.tsv:W2-UNI:LOCL, c7_w2uni_closed.tsv:W2-UNI:RB_M, c7_w2uni_closed.tsv:W2-UNI:SC_M, c7_w2uni_closed.tsv:W2-UNI:TAIL_M, c7_w2uni_closed.tsv:W2-UNI:U-LOC, c7_w2uni_closed.tsv:W2-UNI:U-LOC-Cor, c7_w2uni_closed.tsv:W2-UNI:UNI-0, c7_w2uni_closed.tsv:W2-UNI:UNI-1, claims.tsv:W2-UNI:CD_M, claims.tsv:W2-UNI:CT_M, claims.tsv:W2-UNI:LOCL, claims.tsv:W2-UNI:RB_M, claims.tsv:W2-UNI:SC_M, claims.tsv:W2-UNI:TAIL_M, claims.tsv:W2-UNI:U-LOC, claims.tsv:W2-UNI:U-LOC-Cor, claims.tsv:W2-UNI:UNI-0, claims.tsv:W2-UNI:UNI-1 |
| `Wave2/W2-UNI/STATEMENT.md:57-63` | same | c6_w2_misc.tsv:W2-UNI:U-LOC, c6_w2_misc.tsv:W2-UNI:UNI-1 |
| `Wave2/W2-UNI/STATEMENT.md:59-72` | same | c7_w2uni_closed.tsv:W2-UNI:U-LOC, c7_w2uni_closed.tsv:W2-UNI:U-LOC-Cor, c7_w2uni_closed.tsv:W2-UNI:UNI-1, claims.tsv:W2-UNI:U-LOC, claims.tsv:W2-UNI:U-LOC-Cor, claims.tsv:W2-UNI:UNI-1 |
| `Wave2/W2-UNI/STATEMENT.md:70` | same | c6_w2_misc.tsv:W2-UNI:UNI-1 |
| `Wave2/W2-UNI/STATEMENT.md:72-74` | same | c6_w2_misc.tsv:W2-UNI:UNI-0, c6_w2_misc.tsv:W2-UNI:UNI-P |
| `Wave2/W2-UNI/STATEMENT.md:74-76` | same | c7_w2uni_closed.tsv:W2-UNI:UNI-0, c7_w2uni_closed.tsv:W2-UNI:UNI-1, c7_w2uni_closed.tsv:W2-UNI:UNI-P, claims.tsv:W2-UNI:UNI-0, claims.tsv:W2-UNI:UNI-1, claims.tsv:W2-UNI:UNI-P |
| `Wave2/W2-UNI/STATEMENT.md:76-80` | same | claims.tsv:W2-APP:POST, claims.tsv:W2-APP:Thm-LOC, claims.tsv:W2-UNI:F-UNI |
| `Wave2/W2-UNI/STATEMENT.md:87-91` | same | c7_w2uni_closed.tsv:W2-UNI:UNI-P |

## C. For the recorder
- Rehash on apply (spans unchanged): the 17 rows marked YES in table A that are batch rows (incl. X10 via premise) + W1C-FINAL:Lemma-CAP (patch bump, ERRATUM). W2-FAC-B:L5 and W2-FAC-S5:L5: hash unchanged; edit `short`/`notes` to say delivery is under A:IDEAL-W⁺ (or on 𝔇).
- C-DLV rows: all hashes unchanged (errata appended after the last line or on line 80 of INVENTORY.md, which no registered row cites; C-DLV/reviews/C1_council_opus.md:140 and R06_sweep cite INVENTORY lines 61-69/64-68,80-81 as historical review evidence — line 80's text changes, numbering does not).
- assumptions.tsv: add `A:IDEAL-W+` (row text in `../FUNI_NARROW/A_IDEALW_PLUS.md`) before or with the rehash; add it to the `assumptions` column of the 19 rows.

