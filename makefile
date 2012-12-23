PYTHONBIN = python2
source-dir = test
bin-dir = csc

rendered-pages = $(wildcard $(source-dir)/*.rst)
aggregated-pages = $(source-dir)/agg.yaml $(source-dir)/agg2.yaml $(source-dir)/agg3.yaml
generated-pages = $(source-dir)/generated.spec 

.SECONDARY:
.PHONY: all clean test

content += $(subst .spec,.html,$(generated-pages))
content += $(subst .agg,.html,$(aggregated-pages))
content += $(subst .rst,.html,$(rendered-pages))

all: $(content)

clean:
	-rm -f $(content) $(subst .spec,.agg,$(generated-pages))

%.html:%.rst
	$(PYTHONBIN) $(bin-dir)/csc.py $< $@
%.html:%.txt
	$(PYTHONBIN) $(bin-dir)/csc.py $< $@
%.agg:%.spec
	$(PYTHONBIN) $(bin-dir)/csa.py $< $@
%.txt:%.agg
	$(PYTHONBIN) $(bin-dir)/csa.py $< $@
