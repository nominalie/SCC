# SCC
Supreme Court of Canada citation parser.

Very basic Python scripts to parse "Authors Cited" references in SCC decisions, as formatted at CanLII.org (html pages). Outputs individual citations to a csv file.

Note: File read path is not for CanLII website, which does not permit automated scraping/processing of its content. Contact CanLII directly for permissions and restrictions.

csv file is provided as an example of the ingest file used to iterate through case law corpus, which was stored on local server. File read strategies will depend on user scenario.

After initial iteration, "No Authors Cited section found" rows were identified in output file, and then reprocessed using French regular expression capturing. Another option would be to look for "DC.language" metatag and use French regular expression if fr Dublin Core tag found. However, it was unclear whether this tagging was consistently applied, therefore re-processing was deemed the more reliable option.

This repository is a private project and is in no way associated with CanLII or any official case law reporter.
