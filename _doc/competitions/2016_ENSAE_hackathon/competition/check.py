import sys
sys.path.append("program")
import evaluate
evaluate.private_codalab_wrapper_multi_classification(evaluate.AUC_multi_multi,
                                                      ["orientation", "nature"],
                                                      ".", r".",
                                                      "truth.txt", "answer.txt", use_print=True)
