TOPLEVEL_LANG = verilog
VERILOG_SOURCES = $(shell pwd)/modified_tetris.sv
TOPLEVEL = ModifiedTetris
MODULE = modifiedTetrisTester
include $(shell cocotb-config --makefiles)/Makefile.sim
