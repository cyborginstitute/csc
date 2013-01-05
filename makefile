# Copyright 2012-2013 Sam Kleinman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Sam Kleinman (tychoish)


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
