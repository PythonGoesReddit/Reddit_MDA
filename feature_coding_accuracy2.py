from collections import defaultdict
import Reddit_MDA

sents = {}

with open("sample_sentences.txt", errors = "ignore") as f:
    for line in f:
        sents[line.split("\t")[0]] = line.split("\t")[1].strip("\n")


feats = ['vpast_001', 'vpresperfect_002a', 'vpastperfect_002b', 'vpresent_003', 'advplace_004', 'advtime_position_005a', 'advtime_durfreq_005b', 'profirpers_006', 'prosecpers_007', 'prothirdper_008', 'proit_009', 'prodemons_010', 'proindef_011', 'pverbdo_012', 'whquest_013', 'nominalis_014', 'gerund_015', 'nouns_016', 'passagentl_017', 'passby_018', 'mainvbe_019', 'exthere_020', 'thatvcom_021', 'thatacom_022', 'whclause_023', 'vinfinitive_024', 'vpresentpart_025', 'vpastpart_026', 'vpastwhiz_027', 'vpresentwhiz_028', 'thatresub_029', 'thatreobj_030', 'whresub_031', 'whreobj_032', 'whrepied_033', 'sentencere_034', 'advsubcause_035', 'advsubconc_036', 'advsubcond_037', 'advsubother_038', 'prepositions_039', 'adjattr_040', 'adjpred_041', 'adverbs_042', 'conjuncts_045', 'downtoners_046', 'hedges_047', 'amplifiers_048', 'discpart_050', 'demonstr_051', 'modalsposs_052', 'modalsness_053', 'modalspred_054', 'vpublic_055', 'vprivate_056', 'vsuasive_057', 'vseemappear_058', 'contractions_059', 'thatdel_060', 'strandprep_061', 'vsplitinf_062', 'vsplitaux_063', 'coordphras_064', 'coordnonp_065', 'negsyn_066', 'negana_067', 'hashtag_201', 'link_202', 'interlink_203', 'caps_204', 'vimperative_205', 'lengthening_206', 'emoticons_207', 'question_208', 'exclamation_209', 'comparatives_syn_212', 'superlatives_syn_213', 'comparatives_ana_214', 'superlatives_ana_215', 'reddit_vocab_216', 'vprogressive_217']

p = open("Feature_coding_discrepancies_flair.tsv", "w")
p.write("Feature\tsentence\tManualCount\tAutoCount\n")
p2 = open("Feature_coding_accuracies_flair.tsv", "w")
p2.write("Feature\tAccuracy\tTrue_positives\tFalse_positives\tTrue_negatives\tFalse_negatives\tPrecision\tRecall\tFScore\n")


for feat in feats:
    sent_count = 0
    error_count = 0
    true_pos = 0
    false_pos = 0
    true_neg = 0
    false_neg = 0
    with open("manual_coding_"+ feat + ".txt") as f:
        for line in f:
            sent_count += 1
            numid = line.split("\t")[0]
            manual = int(line.strip("\n").split("\t")[1])
            auto = Reddit_MDA.process_sent(sents[numid], feat)
            if manual!= auto:
                error_count += 1
                p.write("\t".join([feat, sents[numid].strip("'").strip('"'), str(manual), str(auto)]) + "\n")
            if manual > 0 and auto > 0:
                true_pos += 1
            elif manual == 0 and auto > 0:
                false_pos += 1
            elif manual == 0 and auto == 0:
                true_neg += 1
            else:
                false_neg += 1 
    if true_pos > 0:
        precision = true_pos/(true_pos+false_pos)
        recall = true_pos/(true_pos+false_neg)
        Fscore = 2*((precision*recall)/(precision+recall))
        p2.write(feat + "\t" + str((sent_count-error_count)/sent_count) + "\t" + "\t".join([str(true_pos), str(false_pos), str(true_neg), str(false_neg), str(precision), str(recall), str(Fscore)]) + "\n")
    else:
        p2.write(feat + "\t" + str((sent_count-error_count)/sent_count) + "\t" + "\t".join([str(true_pos), str(false_pos), str(true_neg), str(false_neg), "xxx", "xxx", "xxx"]) + "\n")

p.close()
p2.close()
        


