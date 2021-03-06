
# Datasets
Information about the datasets in this directory. 

The structure of this directory is as follows:

```
π¦datasets
 β£ πKGs
 β β£ πfusion_bilingual_KGs
 β β β£ πILLs_fusion
 β β β β£ πmerged_ILLs_KG_en_fr.txt
 β β β β£ πmerged_ILLs_KG_en_zh.txt
 β β β β πmerged_ILLs_KG_zh_fr.txt
 β β β πNMN_fusion
 β β β β£ πmerged_NMN_KG_en_fr.txt
 β β β β£ πmerged_NMN_KG_en_zh.txt
 β β β β πmerged_NMN_KG_zh_fr.txt
 β β πsampled_monolingual_KGs
 β β β£ πSampled_en.txt
 β β β£ πSampled_fr.txt
 β β β πSampled_zh.txt
 β£ πQuestions
 β β£ πen-fr
 β β β£ π2-hop
 β β β β£ πrdf_version
 β β β β β£ πen_fr_2h_en_question_rdf
 β β β β β£ πen_fr_2h_fr_question_rdf
 β β β β β πen_fr_2h_zh_question_rdf
 β β β β£ πen_fr_2h_en_question.txt
 β β β β£ πen_fr_2h_fr_question.txt
 β β β β πen_fr_2h_zh_question.txt
 β β β π3-hop
 β β β β£ πrdf_version
 β β β β β£ πen_fr_3h_en_question_rdf
 β β β β β£ πen_fr_3h_fr_question_rdf
 β β β β β πen_fr_3h_zh_question_rdf
 β β β β£ πen_fr_3h_en_question.txt
 β β β β£ πen_fr_3h_fr_question.txt
 β β β β πen_fr_3h_zh_question.txt
 β β£ πen-zh
 β β β£ π2-hop
 β β β β£ πrdf_version
 β β β β β£ πen_zh_2h_en_question_rdf
 β β β β β£ πen_zh_2h_fr_question_rdf
 β β β β β πen_zh_2h_zh_question_rdf
 β β β β£ πen_zh_2h_en_question.txt
 β β β β£ πen_zh_2h_fr_question.txt
 β β β β πen_zh_2h_zh_question.txt
 β β β π3-hop
 β β β β£ πrdf_version
 β β β β β£ πen_zh_3h_en_question_rdf
 β β β β β£ πen_zh_3h_fr_question_rdf
 β β β β β πen_zh_3h_zh_question_rdf
 β β β β£ πen_zh_3h_en_question.txt
 β β β β£ πen_zh_3h_fr_question.txt
 β β β β πen_zh_3h_zh_question.txt
 β β πzh-fr
 β β β£ π2-hop
 β β β β£ πrdf_version
 β β β β β£ πzh_fr_2h_en_question_rdf
 β β β β β£ πzh_fr_2h_fr_question_rdf
 β β β β β πzh_fr_2h_zh_question_rdf
 β β β β£ πzh_fr_2h_en_question.txt
 β β β β£ πzh_fr_2h_fr_question.txt
 β β β β πzh_fr_2h_zh_question.txt
 β β β π3-hop
 β β β β£ πrdf_version
 β β β β β£ πzh_fr_3h_en_question_rdf
 β β β β β£ πzh_fr_3h_fr_question_rdf
 β β β β β πzh_fr_3h_zh_question_rdf
 β β β β£ πzh_fr_3h_en_question.txt
 β β β β£ πzh_fr_3h_fr_question.txt
 β β β β πzh_fr_3h_zh_question.txt
 β£ πTemplates
 β β£ πen
 β β β£ πen_pattern_body_en.txt
 β β β£ πen_pattern_body_fr.txt
 β β β£ πen_pattern_body_zh.txt
 β β β£ πen_pattern_en.txt
 β β β£ πen_pattern_fr.txt
 β β β πen_pattern_zh.txt
 β β£ πfr
 β β β£ πfr_pattern_body_en.txt
 β β β£ πfr_pattern_body_fr.txt
 β β β£ πfr_pattern_body_zh.txt
 β β β£ πfr_pattern_en.txt
 β β β£ πfr_pattern_fr.txt
 β β β πfr_pattern_zh.txt
 β β πzh
 β β β£ πzh_pattern_body_en.txt
 β β β£ πzh_pattern_body_fr.txt
 β β β£ πzh_pattern_body_zh.txt
 β β β£ πzh_pattern_en.txt
 β β β£ πzh_pattern_fr.txt
 β β β πzh_pattern_zh.txt
 β πREADME.md
```

  ## [`Questions`](Questions) 
  This directory contains all the parallel questions corresponding to the three bilingual KGs of "en-fr","en-zh" and "zh-fr". 
 - All datasets are categorized by the type of questions into different sub-directories.
 - We name each dataset (text file) by its attributes. For example,  `en_fr_2h_en_question` indicates the following attributes for this dataset:
	- `en_fr` means the triples used to construct this dataset are from the English and French versions of DBPedia.
	- `2h` denotes that this question requires 2-hop reasoning.
	- `en_question` means all the questions are in English.
 - We provide each dataset in two formats, one is the standard RDF-format (in `rdf_version` directories), the other is a CSV-like format (`.txt` files) with the following conventions:
	- Each line is a data record.
	- Each data record can be separated by a first-level separator (a TAB character "`	`") into the text of the question, the answer and the reasoning path.
	- The reasoning path can be separated by a second-level separator ("`#`") into triples.
## [`Templates`](Templates)
This directory contains parallel templates (patterns) for relations in English, Chinese and French, in case you find them useful.
## [`KGs`](KGs)
This directory contains all the KGs used in question generation.
- `sampled_monolingual_KGs` contains the sampled KGs using the ICS approach.
- `fusion_bilingual_KGs` contains bilingual KGs that are created through entity alignments, either with IILs (ground truth) or NMN model predictions.