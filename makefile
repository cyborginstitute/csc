############################################################
#
# User configuraiton values.

PYTHONBIN = python2
source-dir = test
build-dir = build
bin-dir = csc

############################################################
#
# Defines page specifications. No configuration needed.

rendered-pages = $(wildcard $(source-dir)/*.rst)
aggregated-pages = $(widlcard $(source-dir)/*.agg)
generated-pages = $(widlcard $(source-dir)/*.spec)
content += $(subst .spec,.html,$(generated-pages))
content += $(subst .agg,.html,$(aggregated-pages))
content += $(subst .rst,.html,$(rendered-pages))
output = $(subst $(source-dir),$(build-dir),$(content))

############################################################
#
#

.SECONDARY:
.PHONY: all clean

all: $(output)
clean:
	-rm -rf $(build-dir)/*
	-rm -rf $(source-dir)/*.yaml

$(build-dir):
	mkdir -p $@
$(build-dir)/%.html:$(source-dir)/%.rst
	$(PYTHONBIN) $(bin-dir)/csc.py $< $@
$(build-dir)/%.html:%.txt
	$(PYTHONBIN) $(bin-dir)/csc.py $< $@
%.agg:%.spec
	$(PYTHONBIN) $(bin-dir)/csa.py $< $@
%.txt:%.agg
	$(PYTHONBIN) $(bin-dir)/csa.py $< $@
