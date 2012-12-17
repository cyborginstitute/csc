PYTHONBIN = python2
source-dir = test
bin-dir = csc

rendered-pages = $(wildcard $(source-dir)/*.rst)
aggregated-pages = $(source-dir)/agg.yaml $(source-dir)/agg2.yaml $(source-dir)/agg3.yaml
generated-pages = $(source-dir)/generated.spec 

.SECONDARY:
.PHONY: all clean test

content += $(subst .spec,.html,$(generated-pages)) 
content += $(subst .yaml,.html,$(aggregated-pages))
content += $(subst .rst,.html,$(rendered-pages)) 

all: $(content)

clean:
	-rm -f $(subst .yaml,.txt,$(generated-pages)) $(wildcard $(source-dir)/*.html) 

%.html:%.rst
	$(PYTHONBIN) $(bin-dir)/csc.py $< $@
%.html:%.txt
	$(PYTHONBIN) $(bin-dir)/csc.py $< $@
%.yaml:%.spec
	$(PYTHONBIN) $(bin-dir)/csa.py $< $@
%.txt:%.yaml
	$(PYTHONBIN) $(bin-dir)/csa.py $< $@
